"""
URL configuration for dhtsensordashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from sensorapp import views
from  authentication import views as vot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('save-data/', views.save_sensor_data, name='save_data'),
    path('',vot.login_view, name='login'),
    path('Home/', views.sensor_data_graph, name='sensor_graph'),
    path('logout/', views.logout_view, name='logout'),
    path('led_control/', views.control_led, name='led_control'),
    path('led_state/', views.led_state, name='led_state'),
]
