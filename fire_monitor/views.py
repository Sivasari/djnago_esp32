from django.http import JsonResponse
from django.shortcuts import render
from .models import FireSensor

import serial
from django.http import JsonResponse
from .models import FireSensor
ESP32_SERVER = "http://192.168.37.153"

# Set up Serial communication with ESP32
#ESP32_PORT = "COM3"  # Change this to the correct port (Windows: COMX, Linux: /dev/ttyUSBX)
BAUD_RATE = 115200

def send_command_to_esp32(command):
    """Sends a command to ESP32 via Serial"""
    try:
        with serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1) as ser:
            ser.write(command.encode())
    except Exception as e:
        print("Error communicating with ESP32:", e)

def fire_status(request):
    latest_status = FireSensor.objects.last()
    fire_detected = latest_status.status if latest_status else False

    # Send fire status to ESP32
    if fire_detected:
        send_command_to_esp32("FIRE_DETECTED")
    else:
        send_command_to_esp32("NO_FIRE")

    return JsonResponse({"fire_detected": fire_detected})




def update_fire_status(request):
    status = request.GET.get('status', 'false') == 'true'
    FireSensor.objects.create(status=status)
    return JsonResponse({'message': 'Fire status updated', 'fire_detected': status})

def fire_monitor_page(request):
    return render(request, 'fire_monitor/fire_monitor.html')  # ✅ Use correct path
