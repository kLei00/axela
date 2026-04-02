## Install the following to the pi using the terminal, run:

### pyaudio speech recognition for speech to text:
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev flac
pip install SpeechRecognition pyaudio

### mpg123 (audio to mp3) and gTTS (google tts) for response tts:
sudo apt-get install mpg123
pip install gTTS

### Picovoice Porcupine for wake word functionality
pip install pvporcupine

### Google genai for Gemini Wrapper
pip install google-generativeai
pip install python-dotenv
