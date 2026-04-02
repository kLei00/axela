# Converts speech to text to use as prompt
# Requires pyaudio SpeechRecognition, run on pi:
# sudo apt-get update
# sudo apt-get install python3-pyaudio portaudio19-dev flac
# pip install SpeechRecognition pyaudio

import speech_recognition as sr

def listen_and_transcribe():
    recognizer = sr.Recognizer()

    # Get default microphone
    with sr.Microphone() as source:
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("Listening... (Speak now!)")
        try:
            # Listen to the user's input
            # timeout: How long to wait for speech to start before giving up
            # phrase_time_limit: Maximum seconds of speech to record
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            
            print("Processing...")
            
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            print(f"You said: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from the service; {e}")
            return None

# Testing
if __name__ == "__main__":
    transcribed_text = listen_and_transcribe()
    if transcribed_text:
        print("\nSuccess! The Gemini Prompt is:")
        print(transcribed_text)