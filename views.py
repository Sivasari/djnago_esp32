from django.http import JsonResponse
import requests
from django.shortcuts import render
import cv2
import mediapipe as mp
import numpy as np
from django.http import JsonResponse
from PIL import Image






def home(request):
    return render(request, "index.html")


ESP32_SERVER = "http://192.168.253.153/device"  # Use your ESP32 IP
  # Replace with your ESP32's IP address

def control_device(request, action, device):
    if action not in ["on", "off"] or device not in ["1", "2"]:
        return JsonResponse({"error": "Invalid request"}, status=400)

    command = f"{action}{device}"  # Example: "on1", "off2"
    try:
        response = requests.get(ESP32_SERVER, params={"command": command})
        return JsonResponse({"message": response.text})
    except requests.exceptions.RequestException:
        return JsonResponse({"error": "ESP32 not reachable"}, status=500)

