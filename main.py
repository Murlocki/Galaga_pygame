import sys
import pygame
from settings import Settings
from ship import Ship

def run_game():
    # Инициализация pygame
    pygame.init()

    # Получаем разрешение экрана
    settings=Settings()
    screen = pygame.display.set_mode((settings.width, settings.heigth))

    # Заголовок окна
    pygame.display.set_caption('Galaga')

    # Создаем корабль игрока
    ship = Ship()
    # Обработка событий от пользователя
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #Заполняем и перерисовываем экран
        screen.fill(settings.background_color)
        ship.blitme()
        pygame.display.flip()
run_game()