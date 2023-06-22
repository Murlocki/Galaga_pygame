import sys
import pygame

def run_game():
    # Инициализация pygame
    pygame.init()

    # Получаем разрешение экрана
    info_object = pygame.display.Info()
    screen = pygame.display.set_mode((info_object.current_w-20, info_object.current_h-20))

    # Заголовок окна
    pygame.display.set_caption('Galaga')

    # Обработка событий от пользователя
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #Заполняем и перерисовываем экран
        screen.fill((255,255,255))
        pygame.display.flip()
run_game()