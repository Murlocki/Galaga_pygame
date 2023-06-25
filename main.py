import sys
import pygame
from time import sleep
from settings import Settings
from Ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
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
def update_bullets(bullets,aliens):
    # Рисуем пули
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Перебираем столкнушвиеся корабли и пули
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

# Создание флота
def get_number_rows(settings,ship_height,alien_height):
    available_space_y = (settings.heigth - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aline_x(settings,alien_width):
    available_space_x = settings.width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(settings,screen,aliens,alien_number,row_number):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = (alien.rect.height - alien.rect.height * row_number)
    aliens.add(alien)

def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    number_alien_x = get_number_aline_x(settings,alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(settings,screen, aliens, alien_number, row_number)


# Проверка достижения флотом края
def check_fleet_edges(settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings,aliens)
            break
def change_fleet_direction(settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.alien_drop_speed
    settings.fleet_direction *= -1

# Обновляем пришельцев и проверяем энд гейм
def ship_hit(settings,stats,screen,ship,aliens, bullets):
    stats.ship_left -= 1
    aliens.empty()
    bullets.empty()

    # Создаем новый флот после перезагрузки
    create_fleet(settings,screen,ship,aliens)
    ship.ship_center()
    sleep(0.5)

def check_aliens_bottom(settings, stats,screen, ship,aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets)
            break

def update_aliens(settings, ship, aliens,stats, screen, bullets):
    check_fleet_edges(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings,stats,screen,ship,aliens,bullets)
    check_aliens_bottom(settings,stats,screen,ship,aliens,bullets)

# Функция обновления экрана
def update_screen(settings,screen,ship,bullets,aliens):
    # Заполняем задний фон
    screen.fill(settings.background_color)

    # Рисуем корабль
    ship.blitme()

    # Рисуем прищельца
    aliens.draw(screen)
    # Рисуем пули
    update_bullets(bullets,aliens)
    if len(aliens) == 0 and len(bullets) == 0:
        create_fleet(settings,screen,ship,aliens)
    # Обновляем экран
    pygame.display.flip()

def run_game():
    # Инициализация pygame
    pygame.init()

    # Получаем разрешение экрана
    settings = Settings()
    stats = GameStats(settings)
    screen = pygame.display.set_mode((settings.width, settings.heigth))

    # Заголовок окна
    pygame.display.set_caption('Galaga')

    # Создаем корабль игрока
    ship = Ship(screen,settings)

    # Создаем пришельцев
    aliens = Group()
    create_fleet(settings,screen,ship, aliens)
    # Создаем группу пуль
    bullets = Group()

    # Основной цикл игры
    while True:
        check_events(ship, settings, screen, bullets)
        ship.update()
        bullets.update()

        update_aliens(settings,ship,aliens,stats,screen,bullets)
        update_screen(settings, screen, ship, bullets,aliens)



run_game()