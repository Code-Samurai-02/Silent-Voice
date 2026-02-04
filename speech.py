import asyncio
import edge_tts
import os

TEXT = "Silent Voice system is ready"
VOICE = "en-US-AriaNeural"
FILE = "speech.mp3"

async def main():
    await edge_tts.Communicate(TEXT, VOICE).save(FILE)
    os.system(f'explorer.exe {FILE}')

asyncio.run(main())
