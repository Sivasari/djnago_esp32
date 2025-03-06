import speech_recognition as sr
import requests
import re
import pyttsx3  # Text-to-Speech

ESP32_SERVER = "http://192.168.253.153"  # Change this to your ESP32 IP

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Device Mapping
devices = {
    "fan": "1",
    "bulb": "2",
    "tv": "3",
    "motor": "4",
    "ac": "5"
}

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def send_command(action, device_id, device_name=None):
    """Send ON/OFF command to ESP32 and provide voice feedback"""
    try:
        url = f"{ESP32_SERVER}/device/{action}/{device_id}/"
        print(f"🔗 Sending request to: {url}")
        response = requests.get(url, timeout=5)
        print(f"✅ Response: {response.status_code} - {response.text}")

        # Speak confirmation
        if device_name:
            speak(f"OK, turning {action} {device_name}")
        else:
            speak(f"OK, turning {action} all devices")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send command: {e}")
        speak("Sorry, I couldn't send the command.")

def process_command(command):
    """Extract devices and action (on/off) from the command"""
    command = command.lower()

    # Check for "turn on all devices" or "turn off all devices"
    if "please turn on all the devices" in command:
        print("🖥️ Turning ON all devices")
        speak("OK, turning on all the devices")
        for device_name, device_id in devices.items():
            send_command("on", device_id, device_name)
        return
    
    if "please turn off all the devices" in command:
        print("🖥️ Turning OFF all devices")
        speak("OK, turning off all the devices")
        for device_name, device_id in devices.items():
            send_command("off", device_id, device_name)
        return

    # Determine action (on/off)
    action = None
    if "turn on" in command or "switch on" in command or "activate" in command:
        action = "on"
    elif "turn off" in command or "switch off" in command or "deactivate" in command:
        action = "off"
    
    if action is None:
        print("⚠️ No valid action (on/off) detected.")
        speak("Sorry, I didn't understand the action.")
        return

    # Find mentioned devices
    matched_devices = [name for name in devices.keys() if re.search(rf"\b{name}\b", command)]

    # Control all devices if "everything" or "all" is mentioned
    if "all" in command or "everything" in command:
        speak(f"OK, turning {action} all the devices")
        send_command(action, "all")
        return

    if matched_devices:
        for device in matched_devices:
            speak(f"OK, turning {action} {device}")
            send_command(action, devices[device], device)
    else:
        print("⚠️ No known device mentioned.")
        speak("I didn't find any device to control.")

def recognize_speech():
    """Recognize voice command"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak a command (e.g., 'Please turn on the fan and TV')...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"🗣️ Detected Command: {command}")
            process_command(command)

        except sr.UnknownValueError:
            print("❌ Could not understand speech.")
            speak("I couldn't understand your command.")
        except sr.RequestError:
            print("⚠️ Error connecting to speech recognition service.")
            speak("There was an error connecting to the speech service.")

# Run the voice recognition loop
while True:
    recognize_speech()
