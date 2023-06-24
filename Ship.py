import pygame

class Ship():
    def __init__(self, screen, settings):
        self.screen = screen
        self.image = pygame.image.load('Ship.bmp')

        # Получаем прямоугольный хитбокс изображения
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
        # Флаги для непрерывного перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.ai_settings = settings

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.speed_factor
        if self.moving_up and self.rect.top > 0:
            self.bottom -= self.ai_settings.speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.speed_factor
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom