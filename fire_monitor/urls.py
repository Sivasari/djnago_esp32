from django.urls import path
from .views import fire_status, update_fire_status, fire_monitor_page

urlpatterns = [
    path('', fire_monitor_page, name='fire_monitor'),
    path('status/', fire_status, name='fire_status'),
    path('update/', update_fire_status, name='update_fire_status'),
]
