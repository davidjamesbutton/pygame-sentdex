import pygame

def load(filename):
    pygame.mixer.music.load(filename)
    # TODO: Remove this hack by reducing loud asset volume
    pygame.mixer.music.set_volume(0.5)

def play():
    pygame.mixer.music.play(-1)

def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()




