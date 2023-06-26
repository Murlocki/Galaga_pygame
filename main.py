import sys
import pygame
from time import sleep
from settings import Settings
from scoreboard import Scoreboard
from Ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from game_stats import GameStats
from pygame.sprite import Group

# Пишем функцию для проверки ивентов
def check_events(ship,settings, screen,bullets,stats,play_button,aliens,sb):
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                sys.exit()
            case pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(stats, play_button, mouse_x, mouse_y,ship,aliens,bullets,settings,screen,sb)
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

# Проверяем нажатие кнопку
def check_play_button(stats, play_button, mouse_x, mouse_y,ship,aliens,bullets,settings,screen,sb):
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(settings,screen,ship,aliens)
        ship.ship_center()
        stats.game_active = True
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
def update_bullets(bullets,aliens,settings,stats,sb):
    # Рисуем пули
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Перебираем столкнушвиеся корабли и пули
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score +=settings.alien_points
    sb.prep_score()
    check_high_score(stats,sb)
def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
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
    if row_number != 0:
        alien.rect.y = (alien.rect.height + alien.rect.height * row_number)
    else:
        alien.rect.y = (alien.rect.height + 4 * alien.rect.height)
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
def ship_hit(settings,stats,screen,ship,aliens, bullets,sb):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()

        # Создаем новый флот после перезагрузки
        create_fleet(settings,screen,ship,aliens)
        ship.ship_center()
        sleep(0.5)
    else:
        stats.game_active = False
        settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(True)

def check_aliens_bottom(settings, stats,screen, ship,aliens, bullets,sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            ship_hit(settings, stats, screen, ship, aliens, bullets,sb)
            break

def update_aliens(settings, ship, aliens,stats, screen, bullets,sb):
    check_fleet_edges(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings,stats,screen,ship,aliens,bullets,sb)
    check_aliens_bottom(settings,stats,screen,ship,aliens,bullets,sb)

# Функция обновления экрана
def update_screen(settings,screen,ship,bullets,aliens,play_button,stats,sb):
    # Заполняем задний фон
    screen.fill(settings.background_color)
    # Рисуем корабль
    ship.blitme()
    # Рисуем прищельца
    aliens.draw(screen)
    # Рисуем пули
    update_bullets(bullets,aliens,settings,stats,sb)
    if len(aliens) == 0 and len(bullets) == 0:
        stats.level +=1
        sb.prep_level()
        settings.increase_speed()
        create_fleet(settings,screen,ship,aliens)
    # Рисуем счет
    sb.show_score()
    # Рисуем кнопку
    if not stats.game_active:
        play_button.draw_button()
    # Обновляем экран
    pygame.display.flip()

def run_game():
    # Инициализация pygame
    pygame.init()

    # Получаем разрешение экрана
    settings = Settings()
    stats = GameStats(settings)
    screen = pygame.display.set_mode((settings.width, settings.heigth))
    sb = Scoreboard(settings, screen, stats)

    # Заголовок окна
    pygame.display.set_caption('Galaga')

    # Создаем кнопку
    play_button = Button(settings,screen,'Play')
    # Создаем корабль игрока
    ship = Ship(screen,settings)

    # Создаем пришельцев
    aliens = Group()
    create_fleet(settings,screen,ship, aliens)
    # Создаем группу пуль
    bullets = Group()

    # Основной цикл игры
    while True:
        check_events(ship, settings, screen, bullets,stats,play_button,aliens,sb)
        if stats.game_active:
            ship.update()
            bullets.update()
            update_aliens(settings,ship,aliens,stats,screen,bullets,sb)
        update_screen(settings, screen, ship, bullets,aliens,play_button,stats,sb)



run_game()