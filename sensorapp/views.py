from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

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
    # Get the last 100 records from the database
    data = SensorData.objects.all().order_by('-timestamp')[:100]
    
    # Prepare data for the charts
    labels = [record.timestamp.strftime('%H:%M:%S') for record in data]
    temp_data = [record.temperature for record in data]
    humidity_data = [record.humidity for record in data]

    return render(request, 'sensorapp/sensor_data_graph.html', {'data': data})

def get_sensor_data(request):
    # Get the last 100 records from the database
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
