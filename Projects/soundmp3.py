import pygame

import threading

def kuchtobolo():
    threading.Timer(5.0, kuchtobolo).start()
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/wall.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    except:
        print("An exception occurred")

kuchtobolo()

