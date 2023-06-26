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

        #Изменение настроек
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    # Метод изменения настроек для сложности
    def initialize_dynamic_settings(self):
        self.speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50
    def increase_speed(self):
        self.speed_factor *=self.speedup_scale
        self.bullet_speed_factor *=self.speed_factor
        self.alien_speed_factor *=self.speed_factor
        self.alien_points = int(self.alien_points * self.score_scale)