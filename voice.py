import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")

samplerate = 16000
duration = 5

print("Listening...")

while True:
    audio = sd.rec(int(duration * samplerate),
                   samplerate=samplerate,
                   channels=1,
                   dtype='float32')
    sd.wait()

    audio = np.squeeze(audio)

    segments, _ = model.transcribe(audio)

    for segment in segments:
        print("Text:", segment.text)