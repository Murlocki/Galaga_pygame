import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,settings,screen,ship):
        super().__init__()
        self.screen=screen

        # Создаем позицию пули
        self.rect=pygame.Rect(0,0,settings.bullet_width,settings.bullet_heigth)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y=float(self.rect.y)
        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    # Перемещение пули
    def update(self):
        self.y -=self.speed_factor
        self.rect.y=self.y

    # Отрисовка пули
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)