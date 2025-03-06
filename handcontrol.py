import cv2
import mediapipe as mp
import requests
import pygame
import os  # For file path management

# ESP32 Server URL
ESP32_SERVER = "http://192.168.253.153"  # Replace with your ESP32 IP

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Start Video Capture
cap = cv2.VideoCapture(0)

# Initialize Pygame Mixer
pygame.mixer.init()

# Define Audio File Paths (Relative)
AUDIO_DIR = os.path.join(os.getcwd(), "audio")  # Adjust if needed
sound_files = {
    "1": os.path.join(AUDIO_DIR, "bulb_on.mp3"),
    "2": os.path.join(AUDIO_DIR, "fan_on.mp3"),
    "3": os.path.join(AUDIO_DIR, "ac_on.mp3"),
    "4": os.path.join(AUDIO_DIR, "tv_on.mp3"),
    "5": os.path.join(AUDIO_DIR, "all_on.mp3"),
    "off": os.path.join(AUDIO_DIR, "all_off.mp3"),
}

def play_sound(device):
    """Play sound for the given device."""
    try:
        sound_file = sound_files.get(device, None)
        if sound_file and os.path.exists(sound_file):
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        else:
            print(f"❌ Audio file not found: {sound_file}")
    except Exception as e:
        print(f"❌ Failed to play sound: {e}")

def send_command(action, device):
    """Send ON/OFF command to ESP32."""
    try:
        url = f"{ESP32_SERVER}/device/{action}/{device}/"
        response = requests.get(url, timeout=2)  # Timeout added
        if response.status_code == 200:
            print(f"✅ Sent: {action} to Device {device} ({url})")
            play_sound(device if action == "on" else "off")  # Play sound
        else:
            print(f"⚠️ Failed to send command: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB for processing
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_hands = hands.process(image)

        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get finger landmarks
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x  # X-axis for thumb

                index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
                middle_base = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
                ring_base = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
                pinky_base = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y
                thumb_base = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x

                # Determine extended fingers
                fingers_extended = [
                    index_tip < index_base,  # Index Finger
                    middle_tip < middle_base,  # Middle Finger
                    ring_tip < ring_base,  # Ring Finger
                    pinky_tip < pinky_base,  # Pinky Finger
                ]
                thumb_extended = thumb_tip > thumb_base  # Thumb check

                num_fingers = fingers_extended.count(True)

                # Gesture Detection
                if num_fingers == 0 and thumb_extended:
                    print("👍 Thumbs-up Detected: Turning ON Device 5")
                    send_command("on", "5")

                elif num_fingers == 0:
                    print("✊ Closed Fist Detected: Turning OFF all devices")
                    for i in range(1, 6):
                        send_command("off", str(i))

                elif num_fingers == 1:
                    print("☝️ One Finger Detected: Turning ON Device 1")
                    send_command("on", "1")

                elif num_fingers == 2:
                    print("✌️ Two Fingers Detected: Turning ON Device 2")
                    send_command("on", "2")

                elif num_fingers == 3:
                    print("🤟 Three Fingers Detected: Turning ON Device 3")
                    send_command("on", "3")

                elif num_fingers == 4:
                    print("🖖 Four Fingers Detected: Turning ON Device 4")
                    send_command("on", "4")

                elif num_fingers == 4 and thumb_extended:
                    print("🖐 Open Palm Detected: Turning ON all devices")
                    for i in range(1, 6):
                        send_command("on", str(i))

        # Display Video Feed
        cv2.imshow("Hand Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release Resources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
