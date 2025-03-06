import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("🎙️ Speak something...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣️ You said: {command}")
    except sr.UnknownValueError:
        print("❌ Could not understand speech.")
    except sr.RequestError:
        print("❌ Check your internet connection.")
