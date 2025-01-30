from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import SensorData
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
import requests

ESP8266_IP = "http://192.168.145.18"

@csrf_exempt  # Disable CSRF for this view
def save_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data.get('temperature')
            humidity = data.get('humidity')

            # Save data to the database
            SensorData.objects.create(temperature=temperature, humidity=humidity)

             # Broadcast new data
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "sensor_data",
                {
                    "type": "send_sensor_data",
                    "data": {
                        "temperature": temperature,
                        "humidity": humidity,
                    },
                }
            )
            return JsonResponse({'status': 'success'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST requests allowed'}, status=405)

def sensor_data_graph(request):
    user = request.user

    # Check if the user is authenticated
    if not user.is_authenticated:
        return redirect('login')  # Replace 'login' with your login URL name

    # Get the last 100 records from the database
    data = SensorData.objects.all().order_by('-timestamp')[:100]

    # Prepare data for the charts
    labels = [record.timestamp.strftime('%H:%M:%S') for record in data]
    temp_data = [record.temperature for record in data]
    humidity_data = [record.humidity for record in data]

    # Calculate daily average temperatures
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
    daily_avg = SensorData.objects.filter(
        timestamp__date=today.date()
    ).aggregate(average_temperature=Avg('temperature'))

    # Calculate weekly average temperatures
    weekly_avg = SensorData.objects.filter(
        timestamp__date__gte=start_of_week.date()
    ).aggregate(average_temperature=Avg('temperature'))

    # Render the template with data
    return render(request, 'sensorapp/sensor_data_graph.html', {
        'data': data,
        'labels': labels,
        'temp_data': temp_data,
        'humidity_data': humidity_data,
        'daily_avg': daily_avg['average_temperature'],
        'weekly_avg': weekly_avg['average_temperature'],
        'user': user,
    })

def led_state(request):
    user = request.user

    # Check if the user is authenticated
    if not user.is_authenticated:
        return redirect('login')  # Replace 'login' with your login URL name
    
    return render(request,'sensorapp/led_control.html',{'user':user})

def get_sensor_data(request):
    # Get the last 100 records from the database
    user = request.user
    data = SensorData.objects.all().order_by('-timestamp')[:100]
    
    # Prepare data for the charts
    labels = [record.timestamp.strftime('%H:%M:%S') for record in data]
    temp_data = [record.temperature for record in data]
    humidity_data = [record.humidity for record in data]
    
    # Return data in JSON format
    return JsonResponse({
        'labels': labels,
        'tempData': temp_data,
        'humidityData': humidity_data
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def control_led(request):
    if request.method == 'POST':
        led_state = {
            'red': request.POST.get('red'),
            'green': request.POST.get('green'),
            'blue': request.POST.get('blue'),
        }
        
        
        try:
            response = requests.post(f'{ESP8266_IP}/control-led', data=led_state, timeout=5)
            if response.status_code == 200:
                # return JsonResponse({"status": "success", "message": "LED state updated successfully."})
                return redirect("led_state")
            else:
                # return JsonResponse({"status": "error", "message": "Failed to update LED state."})
                return redirect("led_state")
        except requests.exceptions.RequestException as e:
            # return JsonResponse({"status": "error", "message": str(e)})
            return redirect("led_state")
    # return JsonResponse({"status": "error", "message": "Invalid request method."})
    return redirect("led_state")


