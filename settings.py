# Параметры настроек
import pygame
def Resolution_return():
    info_object = pygame.display.Info()
    return info_object.current_w, info_object.current_h
class Settings():
    def __init__(self):
        self.background_color = (255,255,255)
        self.width, self.heigth = Resolution_return()

        # Параметры движения
        self.speed_factor = 1.5

        # Параметры пули
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_heigth = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5