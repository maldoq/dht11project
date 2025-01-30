from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("sensor_graph")  # Redirigez vers une page après connexion
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, "authentication/login.html")