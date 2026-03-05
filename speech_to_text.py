import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import queue
import threading

model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16"
)

samplerate = 16000
block_duration = 2
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    q.put(indata.copy())

def transcribe_worker():
    while True:
        audio = q.get()
        audio = np.squeeze(audio)
        segments, _ = model.transcribe(
            audio,
            language="en",
            beam_size=5
        )
        for segment in segments:
            print(">>", segment.text)

threading.Thread(target=transcribe_worker, daemon=True).start()

with sd.InputStream(
    samplerate=samplerate,
    channels=1,
    dtype="float32",
    blocksize=int(samplerate * block_duration),
    callback=audio_callback
):
    print("Listening...")
    while True:
        pass    