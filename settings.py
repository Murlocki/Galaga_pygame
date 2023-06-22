# Параметры настроек
import pygame
def Resolution_return():
    info_object = pygame.display.Info()
    return info_object.current_w, info_object.current_h
class Settings():
    def __init__(self):
        self.background_color = (255,255,255)
        self.width, self.heigth = Resolution_return()