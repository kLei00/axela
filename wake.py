# Wait for wake phrase to start listening
# Requires pvporcupine, run on pi:
# pip install pvporcupine

import pvporcupine
import pyaudio
import struct
import os
from dotenv import load_dotenv

load_dotenv()

def wait_for_wake_word():
    access_key = os.environ.get("PICOVOICE_ACCESS_KEY")
    if not access_key:
        raise ValueError("Please provide a PICOVOICE_ACCESS_KEY in your .env file.")

    keyword = "knockoff alexa"
    
    try:
        # Initialize Porcupine
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=[keyword]
        )
    except pvporcupine.PorcupineInvalidArgumentError as e:
        print(f"Invalid Access Key: {e}")
        return False

    # Initialize PyAudio to capture the microphone stream
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print(f"\nListening for wake word: '{keyword}'...")

    try:
        while True:
            # Read a chunk of audio from the mic
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            # Process the audio chunk
            keyword_index = porcupine.process(pcm)
            
            # If keyword_index is >= 0, the wake word was heard
            if keyword_index >= 0:
                print(f"\nWake word '{keyword}' detected!")
                return True
                
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()