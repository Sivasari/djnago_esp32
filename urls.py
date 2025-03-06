from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name="home"),  # This will serve the index.html page
    path('device/<str:action>/<str:device>/', views.control_device, name="control_device"),
]
