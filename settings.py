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
        self.alien_speed_factor = 1
        self.alien_drop_speed = 10
        self.fleet_direction = 1

        # Параметры пули
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_heigth = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Количество жизней
        self.ship_limit = 3