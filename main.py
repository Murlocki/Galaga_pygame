import sys
import pygame
from settings import Settings
from Ship import Ship
from bullet import Bullet
from pygame.sprite import Group

# Пишем функцию для проверки ивентов
def check_events(ship,settings, screen,bullets):
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                sys.exit()
            case pygame.KEYDOWN:
                check_keydown_events(event,ship, settings, screen, bullets)
            case pygame.KEYUP:
                check_keyup_events(event,ship)


def check_keydown_events(event, ship, settings, screen, bullets):
    match event.key:
        case pygame.K_RIGHT:
            ship.moving_right = True
        case pygame.K_LEFT:
            ship.moving_left = True
        case pygame.K_UP:
            ship.moving_up = True
        case pygame.K_DOWN:
            ship.moving_down = True
        case pygame.K_SPACE:
            if len(bullets) < settings.bullets_allowed:
                new_bullet = Bullet(settings, screen, ship)
                bullets.add(new_bullet)

def check_keyup_events(event, ship):
    match event.key:
        case pygame.K_RIGHT:
            ship.moving_right = False
        case pygame.K_DOWN:
            ship.moving_down = False
        case pygame.K_UP:
            ship.moving_up = False
        case pygame.K_LEFT:
            ship.moving_left = False

# Обновление пуль
def update_bullets(bullets):
    # Рисуем пули
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
# Функция обновления экрана
def update_screen(settings,screen,ship,bullets):
    # Заполняем задний фон
    screen.fill(settings.background_color)

    # Рисуем корабль
    ship.blitme()

    # Рисуем пули
    update_bullets(bullets)
    # Обновляем экран
    pygame.display.flip()

def run_game():
    # Инициализация pygame
    pygame.init()

    # Получаем разрешение экрана
    settings = Settings()
    screen = pygame.display.set_mode((settings.width, settings.heigth))

    # Заголовок окна
    pygame.display.set_caption('Galaga')

    # Создаем корабль игрока
    ship = Ship(screen,settings)

    # Создаем группу пуль
    bullets = Group()
    # Основной цикл игры
    while True:
        check_events(ship, settings, screen, bullets)
        ship.update()
        bullets.update()
        update_screen(settings, screen, ship, bullets)



run_game()