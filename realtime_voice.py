from TTS.api import TTS
import sounddevice as sd
import numpy as np

# Load model once (global)
print("Loading TTS model...")
tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False)
print("TTS Ready.")

def speak(text: str):
    wav = tts.tts(text)
    wav = np.array(wav, dtype=np.float32)
    sd.play(wav, samplerate=22050)
    sd.wait()


# Only runs if file executed directly
if __name__ == "__main__":
    while True:
        text = input("Enter text (type exit to quit): ")
        if text.lower() == "exit":
            break
        speak(text)