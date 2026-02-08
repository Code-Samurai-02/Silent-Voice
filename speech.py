import asyncio
import edge_tts
import os

TEXT1 = "I'm sahil"
TEXT2 = "This is our project Silent voice"
TEXT3 = "Thank You"
VOICE = "en-US-AriaNeural"
FILE = "speech.mp3"

async def main():
    a = int(input("-->"))
    if(a == 1):
        await edge_tts.Communicate(TEXT1, VOICE).save(FILE)
        os.system(f'explorer.exe {FILE}')
    elif (a == 2):
        await edge_tts.Communicate(TEXT2, VOICE).save(FILE)
        os.system(f'explorer.exe {FILE}')
    elif(a == 3):
        await edge_tts.Communicate(TEXT3, VOICE).save(FILE)
        os.system(f'explorer.exe {FILE}')
    
while True:
    asyncio.run(main())
