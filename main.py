from pathlib import Path
import random
import pygame
import game_objects

MAX_FPS = 100
FPS = 30
ALLOWFIRE = pygame.event.custom_type()
ALIEN_BEGIN_X = 100
ALIEN_BEGIN_Y = 100

def init_aliens(aliens, ship):
    for posx in range(ALIEN_BEGIN_X, ALIEN_BEGIN_X + 500, 50):
        for posy in range(ALIEN_BEGIN_Y, ALIEN_BEGIN_Y + 200, 50):
            aliens.add(game_objects.Alien(path, screen, pygame.Vector2(posx, posy), ship))

def bomb_fall(aliens, bombs):
    for alien in aliens:
        if random.randint(0, 1000) == 1:
            bomb = game_objects.Bomb(screen, alien, mov_ship)
            bomb.fire()
            bombs.add(bomb)

def show_lives(n, screen):
    POS_X = 50
    POS_Y = 50
    SPACE = 20
    path = Path('images')
    ship_path = path.joinpath('ship_straight.png')
    img_ship = pygame.image.load(ship_path)
    posx = POS_X
    for i in range(0, n):
        rect = pygame.Rect(posx, POS_Y, 20, 20)
        screen.blit(img_ship, rect)
        posx += SPACE
    
    

if __name__ == '__main__':
    pygame.init()
    live_numb = 3
    delta = 0.0
    screen = pygame.display.set_mode((640, 480),
                                     # pygame.FULLSCREEN
                                     )
    clock = pygame.time.Clock()
    pygame.time.set_timer(ALLOWFIRE, 1000)
    running = True
    path = Path('images').joinpath('alien1.png')
    aliens = set()
    mov_ship = game_objects.Ship(screen)
    init_aliens(aliens, mov_ship)
    bullets = set()
    bombs = set()
    allow_fire = False
    while running:
        run_objects = []
        run_objects.append(mov_ship)
        run_objects.extend(aliens)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ALLOWFIRE:
                allow_fire = True
        if pygame.key.get_pressed()[pygame.K_SPACE] and allow_fire:
            bullet = game_objects.Missile(screen, mov_ship, aliens)
            bullet.fire()
            bullets.add(bullet)
            allow_fire = False
        run_objects.extend(bullets)
        bomb_fall(aliens, bombs)
        run_objects.extend(bombs)
        for obj in run_objects:
            obj.move()
        for bomb in bombs:
            if bomb.is_hit():
                live_numb -= 1
                break
        for alien in aliens:
            if alien.touch_ship():
                aliens = aliens - {alien}
                live_numb -= 1
                break
        for alien in {al for al in aliens if al.is_fallen == False}:
            alien.fallen()
        for alien in aliens:
            alien.alien_is_out()
        # draw
        screen.fill('black')
        for obj in run_objects:
            obj.draw()
        show_lives(live_numb, screen)
        end_bullets = {b for b in bullets if not b.visible}
        bullets = bullets - end_bullets
        end_bombs = {bomb for bomb in bombs if not bomb.visible}
        bombs = bombs - end_bombs
        delta += clock.tick(MAX_FPS)/1000
        while delta > 1.0/FPS:
            delta -= 1.0/FPS
        pygame.display.flip()
        if live_numb <= 0:
            running = False
    pygame.quit()
