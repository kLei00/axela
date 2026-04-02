# main function
# 1. Wait for wake word "knockoff alexa"
# 1. Get input from stt, converts speech to text
# 2. Send input to wrapper, gets response as text
# 3. Sends response to tts, reads out response

from wake import wait_for_wake_word
from stt import listen_and_transcribe
from wrapper import GeminiBrain
from tts import speak_text

def run_assistant():
    print("--- Starting Assistant ---")
    
    # Initialize Gemini
    try:
        ai = GeminiBrain()
        print("Gemini initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Gemini: {e}")
        return

    speak_text("Systems online. Waiting for wake word.")

    while True:
        # 1. Listen for Wake Word ("knockoff alexa")
        if wait_for_wake_word():
            
            # 2. Play a prompt to indicate it's listening
            speak_text("How can I help?")
            
            # Add a tiny delay to ensure the microphone hardware is fully 
            # released by the wake word script before STT tries to grab it
            time.sleep(0.2)
            
            # 3. Record audio and convert to text
            user_text = listen_and_transcribe()
            
            if user_text:
                # Manual shutdown "shut down"
                if "shut down" in user_text.lower():
                    speak_text("Shutting down. Goodbye!")
                    break
                    
                # 4. Send text to the AI API
                print("Sending to Gemini...")
                ai_response_text = ai.generate_response(user_text)
                
                # 5. Convert AI text to audio and play it
                if ai_response_text:
                    speak_text(ai_response_text)

if __name__ == "__main__":
    try:
        run_assistant()
    except KeyboardInterrupt:
        print("\nAssistant stopped manually.")