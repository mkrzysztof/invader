from pathlib import Path
import random
import pygame
import game_objects

MAX_FPS = 100
FPS = 30
ALLOWFIRE = pygame.event.custom_type()


if __name__ == '__main__':
    pygame.init()
    delta = 0.0
    screen = pygame.display.set_mode((640, 480),
                                     # pygame.FULLSCREEN
                                     )
    clock = pygame.time.Clock()
    pygame.time.set_timer(ALLOWFIRE, 1000)
    running = True
    path = Path('images').joinpath('alien1.png')
    aliens = set()
    for posx in range(100, 600, 50):
        for posy in range(100, 300, 50):
            aliens.add(game_objects.Alien(path, screen, pygame.Vector2(posx, posy)))
    mov_ship = game_objects.Ship(screen)
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
        for alien in aliens:
            if random.randint(0, 10000) == 1:
                bomb = game_objects.Bomb(screen, alien, mov_ship)
                bomb.fire()
                bombs.add(bomb)
        run_objects.extend(bombs)
        for obj in run_objects:
            obj.move()
        for alien in {al for al in aliens if al.is_fallen == False}:
            alien.fallen()
        for alien in aliens:
            alien.alien_is_out()
        # draw
        screen.fill('black')
        for obj in run_objects:
            obj.draw()
        end_bullets = {b for b in bullets if not b.visible}
        bullets = bullets - end_bullets
        end_bomb = {b for b in bombs if not b.visible}
        delta += clock.tick(MAX_FPS)/1000
        while delta > 1.0/FPS:
            delta -= 1.0/FPS
        pygame.display.flip()    
