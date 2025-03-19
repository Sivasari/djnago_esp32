from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('iot.urls')),  # Include the iot app URLs at the root
    path('fire_monitor/', include('fire_monitor.urls')),  # Fix by adding 'fire_monitor/'
]
