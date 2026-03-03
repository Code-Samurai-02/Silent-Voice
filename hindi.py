from TTS.api import TTS

# Load multilingual model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

# Hindi text
text = "नमस्ते, यह एक तेज़ हिंदी टेक्स्ट टू स्पीच सिस्टम है।"

# Generate speech
tts.tts_to_file(
    text=text,
    speaker="female",      # optional
    language="hi",
    file_path="output.wav"
)