from pathlib import Path
import random
import pygame
import game_objects

ALLOWFIRE = pygame.event.custom_type()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    pygame.time.set_timer(game_objects.ALIENMOVE, 100)
    pygame.time.set_timer(game_objects.MISSILLEMOVE, 20)
    pygame.time.set_timer(game_objects.SHIPMOVE, 20)
    pygame.time.set_timer(game_objects.BOMBMOVE, 10)
    pygame.time.set_timer(ALLOWFIRE, 1000)
    BOMBALLOW = pygame.event.custom_type()
    pygame.time.set_timer(BOMBALLOW, 1000)
    pygame.event.set_allowed([pygame.KEYDOWN, game_objects.ALIENMOVE,
                              pygame.QUIT])
    pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP,
                              pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
                              pygame.WINDOWENTER, pygame.WINDOWTAKEFOCUS,
                              pygame.WINDOWLEAVE,pygame.ACTIVEEVENT,
                              pygame.TEXTINPUT, pygame.TEXTEDITING,])
    running = True
    path = Path('images').joinpath('alien1.png')
    aliens = set()
    for posx in [100, 150, 200, 250, 300, 350]:
        aliens.add(game_objects.Alien(path, screen, pygame.Vector2(posx, 100)))
    mov_ship = game_objects.Ship(screen)
    pygame.key.set_repeat(100)
    bullets = set()
    bombs = set()
    allow_fire = False
    while running:
        screen.fill('black')
        events = pygame.event.get()
        for event in events:
            run_objects = []
            run_objects.append(mov_ship)
            run_objects.extend(aliens)
            if event.type == pygame.QUIT:
                running = False
            if event.type == ALLOWFIRE:
                allow_fire = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and allow_fire:
                    bullet = game_objects.Missile(screen, mov_ship, aliens)
                    bullet.fire()
                    bullets.add(bullet)
                    allow_fire = False
            run_objects.extend(bullets)
            for alien in aliens:
                if random.randint(0, 1) == 1 and event.type == BOMBALLOW:
                    bomb = game_objects.Bomb(screen, alien)
                    bomb.fire()
                    bombs.add(bomb)
            run_objects.extend(bombs)
            for obj in run_objects:
                obj.move(event)
        # draw
        for obj in run_objects:
            obj.draw()
        end_bullets = {b for b in bullets if not b.visible}
        bullets = bullets - end_bullets
        end_bomb = {b for b in bombs if not b.visible}
        a = clock.tick()
        pygame.time.delay(20-a)
        pygame.display.flip()
    
