import asyncio
import edge_tts
import pygame
import threading

async def _speak(text):
    communicate = edge_tts.Communicate(text, voice="en-GB-RyanNeural", rate="+15%")
    await communicate.save("output.mp3")

def speak(text):
    print(text)
    asyncio.run(_speak(text))

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    #remove output.mp3 after playing
    pygame.mixer.music.unload()





