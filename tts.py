# Converts text to speech, reads out Gemini's response
# Requires gTTS and mpg123, run on pi:
# sudo apt-get install mpg123
# pip install gTTS

from gtts import gTTS
import os

def speak_text(text):
    if not text:
        return
        
    print(f"Assistant says: {text}")
    
    try:
        # Generate audio
        tts = gTTS(text=text, lang='en', slow=False)
        filename = "response.mp3"
        
        # Save audio file as mp3
        tts.save(filename)
        
        # Play the audio file using mpg123
        os.system(f"mpg123 -q {filename}")
        
        # Clean up the audio file
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        print(f"Error playing audio: {e}")

# Testing
if __name__ == "__main__":
    test_phrase = "Hello! I am your new Raspberry Pi voice assistant. My brain is powered by Gemini."
    speak_text(test_phrase)