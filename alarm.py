import pygame
import time


def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
