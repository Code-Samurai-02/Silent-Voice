from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np

model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16"
)

samplerate = 16000
duration = 3

print("Listening...")

while True:
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()

    audio = np.squeeze(audio)

    segments, _ = model.transcribe(audio)

    for seg in segments:
        print("Speech:", seg.text)