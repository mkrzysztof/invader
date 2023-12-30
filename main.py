from pathlib import Path
import random
import pygame
import game_objects
import board
from collections import namedtuple

Position = namedtuple('Position', ['x', 'y'])

MAX_FPS = 100
FPS = 30
ALLOWFIRE = pygame.event.custom_type()


ALIEN_BOMB_FREQUECY = 1000

alien_on_board = [
"""oxxxxxxxxx
xxxxxxxxxo
xoxoxoxoxo
xxooxxooxx""",
"""xoxoxoxoxo
xxooooooxx
xxxxxxxxxx""",
    ]

def bomb_fall(aliens, bombs, ship, screen):
    for alien in aliens:
        if random.randint(0, ALIEN_BOMB_FREQUECY) == 1:
            bomb = game_objects.Bomb(screen, alien, ship)
            bomb.fire()
            bombs.add(bomb)

def show_lives(n, screen):
    POS = Position(x=50, y=50)
    SPACE = 20
    path = Path('images')
    ship_path = path.joinpath('ship_straight.png')
    img_ship = pygame.image.load(ship_path)
    posx = POS.x
    for i in range(0, n):
        rect = pygame.Rect(posx, POS.y, 20, 20)
        screen.blit(img_ship, rect)
        posx += SPACE
    

def welcome_page(screen):
    pygame.event.clear()
    screen.fill('black')
    def_font_name =  pygame.font.get_default_font()
    font = pygame.font.SysFont(def_font_name, 20)
    surf = font.render('Title Screen', True, pygame.Color(255, 0, 0))
    running = True
    rect = surf.get_rect()
    rect.move_ip(100, 100)
    screen.blit(surf, rect)
    pygame.display.flip()
    while running:
        pygame.event.clear()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            running = False

def gameover_page(screen):
    def_font_name =  pygame.font.get_default_font()
    font = pygame.font.SysFont(def_font_name, 20)
    surf = font.render('Game Over', True, pygame.Color(0, 255, 0))
    running = True
    rect = surf.get_rect()
    rect.move_ip(200, 200)
    screen.blit(surf, rect)
    pygame.display.flip()
    while running:
        pygame.event.clear()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            running = False
    pygame.time.delay(500)
    
    
class TimeStruct:
    def __init__(self):
        self.delta = 0
        self.clock = pygame.time.Clock()

class ShipObjects:
    def __init__(self, screen):
        self.bullets = set()
        self.ship = game_objects.Ship(screen)

class AliensObjects:
    def __init__(self):
        self.aliens = set()
        self.bombs = set()

    def fall(self):
        for alien in {al for al in self.aliens if not al.is_fallen}:
            alien.fallen()

    def put_to_start_position(self):
        for alien in self.aliens:
            alien.put_to_start_pos()

    def bombs_fall(self, screen, ship):
        for alien in self.aliens:
            if random.randint(0, ALIEN_BOMB_FREQUECY) == 1:
                bomb = game_objects.Bomb(screen, alien, ship)
                bomb.fire
        

class GameParameters:
    def __init__(self):
        self.live_numb = 3
        self.running = True
        self.allow_fire = False
        self.points = 0

    def event_catch(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_parameters.running = False
            if event.type == ALLOWFIRE:
                game_parameters.allow_fire = True

    def show_point(self, screen):
        font = pygame.font.SysFont('', 20)
        points = font.render(str(self.points), True, pygame.Color(0, 255,0))
        rect = points.get_rect()
        rect.move_ip(200, 100)
        screen.blit(points, rect)

def main_in_loop(screen, time_struct, ship_objects, aliens_objects,
                 game_parameters):
    run_objects = []
    run_objects.append(ship_objects.ship)
    run_objects.extend(aliens_objects.aliens)
    game_parameters.event_catch()
    if game_parameters.allow_fire:
        game_parameters.allow_fire = False
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            missile_position = pygame.Vector2(ship_objects.ship.rect.midtop)
            bullet = game_objects.Missile(screen,
                                          missile_position,
                                          aliens_objects.aliens)
            bullet.fire()
            ship_objects.bullets.add(bullet)
    run_objects.extend(ship_objects.bullets)
    bomb_fall(aliens_objects.aliens, aliens_objects.bombs, ship_objects.ship,
              screen)
    run_objects.extend(aliens_objects.bombs)
    for obj in run_objects:
        is_hit = obj.move()
        if is_hit:
            game_parameters.points += 10
    pause_on_hit = False
    for bomb in aliens_objects.bombs:
        if bomb.is_hit():
            game_parameters.live_numb -= 1
            pause_on_hit = True
            break
    for alien in aliens_objects.aliens:
        if alien.touch_ship(ship_objects.ship):
            aliens_objects.aliens -= {alien}
            game_parameters.live_numb -= 1
            pause_on_hit = True
            break
    aliens_objects.fall()
    aliens_objects.put_to_start_position()
    screen.fill('black')
    for obj in run_objects:
        obj.draw()
    show_lives(game_parameters.live_numb, screen)
    game_parameters.show_point(screen)
    end_bullets = {b for b in ship_objects.bullets if not b.visible}
    ship_objects.bullets -= end_bullets
    bombs = aliens_objects.bombs
    end_bombs = {bomb for bomb in bombs if not bomb.visible}
    bombs -= end_bombs
    time_struct.delta += time_struct.clock.tick(MAX_FPS)/1000
    while time_struct.delta > 1.0/FPS:
        time_struct.delta -= 1.0/FPS
    pygame.display.flip()
    if pause_on_hit:
        pygame.time.delay(1000)
        
if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.key.set_repeat()
    screen = pygame.display.set_mode((640, 480),
                                     # pygame.FULLSCREEN
                                     )
    board_numb = 0
    while True:
        welcome_page(screen)
        game_parameters = GameParameters()
        for brd in alien_on_board:
            time_struct = TimeStruct()
            pygame.time.set_timer(ALLOWFIRE, 100)
            aliens_objects = AliensObjects()
            ship_objects = ShipObjects(screen)
            gb = board.GameBoard(aliens_objects.aliens,
                                 brd,
                             screen)
            gb.put()
            while game_parameters.running:
                main_in_loop(screen, time_struct, ship_objects,
                             aliens_objects,
                             game_parameters)
                if game_parameters.live_numb <= 0:
                    game_parameters.running = False
                if not aliens_objects.aliens:
                    board_numb += 1
                    break
                if not game_parameters.running:
                    gameover_page(screen)
    pygame.quit()
