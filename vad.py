import torch
from silero_vad import load_silero_vad, get_speech_timestamps

# Load VAD model once
vad_model = load_silero_vad()

def detect_speech(audio, sample_rate=16000):
    """
    Returns True if speech is detected
    """
    audio_tensor = torch.from_numpy(audio)

    speech = get_speech_timestamps(
        audio_tensor,
        vad_model,
        sampling_rate=sample_rate
    )

    return len(speech) > 0