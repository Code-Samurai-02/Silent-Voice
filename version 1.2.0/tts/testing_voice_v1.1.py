from kokoro import KPipeline
import sounddevice as sd

# Load model once
pipeline = KPipeline(lang_code="a")

print("Kokoro TTS ready.")
print("Type text and press Enter. Type 'exit' to quit.\n")



while True:
    text = input("You: ").strip()

    if text.lower() == "exit":
        break

    if not text:
        continue

    print("Speaking...")

    for _, _, audio in pipeline(
        text,
        voice="af_heart"
    ):
        sd.play(audio, 24000)
        sd.wait()

print("TTS stopped.")