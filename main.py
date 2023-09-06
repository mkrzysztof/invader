from pathlib import Path
import pygame
import game_objects

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    pygame.time.set_timer(game_objects.ALIENMOVE, 100)
    pygame.time.set_timer(game_objects.MISSILLEMOVE, 20)
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
        aliens.add(game_objects.Alien(path, screen, (posx, 100)))
    mov_ship = game_objects.Ship(screen)
    pygame.key.set_repeat(100)
    bullets = set()
    while running:
        screen.fill('black')
        events = pygame.event.get()
        print(events)
        for event in events:
            run_objects = []
            run_objects.append(mov_ship)
            run_objects.extend(aliens)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = game_objects.Missile(screen, mov_ship, aliens)
                    bullet.fire()
                    bullets.add(bullet)
            run_objects.extend(bullets)
            for obj in run_objects:
                obj.move(event)
        # draw
        for obj in run_objects:
            obj.draw()
        end_bullets = {b for b in bullets if not b.bang}
        bullets = bullets - end_bullets
        clock.tick(20)
        pygame.display.flip()
        pygame.time.delay(10)
    
