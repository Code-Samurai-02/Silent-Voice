import time
import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel


# =============================
# Settings
# =============================
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 3

AUDIO_FILE = "recording.wav"


# =============================
# Load model
# =============================
print("Loading Whisper model...")

model = WhisperModel(
    "large-v3-turbo",
    device="cuda",
    compute_type="float16"
)

print("Model loaded successfully.")
print("Starting continuous speech recognition...")
print("Press Ctrl+C to stop.\n")


# =============================
# Continuous STT
# =============================
try:
    while True:

        print("Listening...")

        # Record audio
        audio = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16"
        )

        sd.wait()

        # Save audio
        wav.write(
            AUDIO_FILE,
            SAMPLE_RATE,
            audio
        )

        # Transcribe
        segments, info = model.transcribe(
            AUDIO_FILE,
            language="en",
            beam_size=5
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        # Print result
        if text.strip():
            print(f"Speech: {text}")
        else:
            print("No speech detected.")

        print()

except KeyboardInterrupt:
    print("\nSTT stopped.")