import pygame

class Effect:
    def __init__(self):
        pygame.mixer.init()

    def sound(self, filestr):
        pygame.mixer.music.load(filestr)
        pygame.mixer.music.play()

    def busy(self):
        return pygame.mixer.music.get_busy()
