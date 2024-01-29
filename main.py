from collections import namedtuple
from enum import Enum, auto
from pathlib import Path
from os import path
import random
import pygame
from pygame import gfxdraw
import game_objects
import board
import screen_field

Position = namedtuple('Position', ['x', 'y'])


class MovingType(Enum):
    MOVE = auto()
    FIRE = auto()


Moving = namedtuple('Moving', ['type', 'move'])


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

def bomb_fall(aliens, bombs, ship, display, screen_fields):
    for alien in aliens:
        if random.randint(0, ALIEN_BOMB_FREQUECY) == 1:
            bomb = game_objects.Bomb(display, alien, ship, screen_fields)
            bomb.fire()
            bombs.add(bomb)

def show_lives(n, display):
    POS = Position(x=50, y=50)
    SPACE = 20
    pth = Path(path.abspath('images'))
    ship_path = pth.joinpath('ship_straight.png')
    img_ship = pygame.image.load(ship_path)
    posx = POS.x
    for _ in range(0, n):
        rect = pygame.Rect(posx, POS.y, 20, 20)
        display.blit(img_ship, rect)
        posx += SPACE


def welcome_page(display):
    pygame.event.clear()
    display.fill('black')
    def_font_name =  pygame.font.get_default_font()
    font = pygame.font.SysFont(def_font_name, 20)
    surf = font.render('Title Screen', True, pygame.Color(255, 0, 0))
    running = True
    rect = surf.get_rect()
    rect.move_ip(100, 100)
    display.blit(surf, rect)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.FINGERDOWN:
                running = False
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            running = False

def gameover_page(display):
    def_font_name =  pygame.font.get_default_font()
    font = pygame.font.SysFont(def_font_name, 20)
    surf = font.render('Game Over', True, pygame.Color(0, 255, 0))
    running = True
    rect = surf.get_rect()
    rect.move_ip(200, 200)
    display.blit(surf, rect)
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
    def __init__(self, display, screen_fields):
        self.bullets = set()
        self.ship = game_objects.Ship(display, screen_fields)

class AliensObjects:
    def __init__(self, aliens):
        self.aliens = set(aliens)
        self.bombs = set()

    def fall(self):
        for alien in {al for al in self.aliens if not al.is_fallen}:
            alien.fallen()

    def put_to_start_position(self):
        for alien in self.aliens:
            alien.put_to_start_pos()

    def bombs_fall(self, display, ship, screen_fields):
        for alien in self.aliens:
            if random.randint(0, ALIEN_BOMB_FREQUECY) == 1:
                bomb = game_objects.Bomb(display, alien, ship, screen_fields)
                bomb.fire()


class GameParameters:
    def __init__(self, game_board):
        self.live_numb = 3
        self.running = True
        self.allow_fire = False
        self.points = 0
        self.left_rect = None
        self.right_rect = None
        self.background = None
        self.game_board = game_board
        self._draw_background()
        self._posx = game_board.screen_fields.joyfield.center[0]
        self._finger_down = False
        self._used_space = False

    def _draw_background(self):
        rect_screen = self.game_board.screen.get_rect()
        pos_left_rect = (
            (rect_screen.bottomleft[0] + rect_screen.midbottom[0])/2,
            (rect_screen.midleft[1] + rect_screen.bottomleft[1])/2
        )
        pos_right_rect = (
            (rect_screen.midbottom[0] + rect_screen.bottomright[0])/2,
            (rect_screen.midbottom[1] + rect_screen.center[1])/2
        )
        self.background = pygame.Surface(rect_screen.size)
        self.background.fill('black')
        size = (20, 20)
        self.left_rect = pygame.Rect(pos_left_rect, size)
        self.right_rect = pygame.Rect(pos_right_rect, size)
        gfxdraw.box(self.background, self.game_board.screen_fields.joyfield,
                    pygame.Color('blue'))
        gfxdraw.box(self.background, self.game_board.screen_fields.firefield,
                    pygame.Color('blue'))
        gfxdraw.filled_circle(self.background,
                              *self.game_board.screen_fields.joyfield.center,
                              3, pygame.Color('gold'))


    def event_catch(self):
        move_type = set()
        move = 0
        EPS = 3
        scale_x = self.game_board.screen.get_width()
        center = self.game_board.screen_fields.joyfield.center[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == ALLOWFIRE:
                self.allow_fire = True
            elif event.type == pygame.FINGERDOWN:
                print(event)
                self._finger_down = True
            elif event.type == pygame.FINGERUP:
                self._finger_down = False
            elif event.type == pygame.FINGERMOTION:
                print(event)
                move_type.add(MovingType.MOVE)
                self._posx = event.x * scale_x
        if self._posx - center > EPS + 2:
            move = 1
        elif self._posx - center < -EPS - 2:
            move = -1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move = -1
            move_type.add(MovingType.MOVE)
        if keys[pygame.K_RIGHT]:
            move = 1
            move_type.add(MovingType.MOVE)
        if keys[pygame.K_SPACE]:
            self._finger_down = True
            self._used_space = True
        else:
            if self._used_space:
                self._finger_down = False
        if self._finger_down:
            print("hej")
            move_type.add(MovingType.FIRE)
        return Moving(move_type, move)

    def show_point(self, display):
        font = pygame.font.SysFont('', 20)
        points = font.render(str(self.points), True, pygame.Color(0, 255,0))
        rect = points.get_rect()
        rect.move_ip(200, 100)
        display.blit(points, rect)

def ship_fire(param_game, obj_game, objs_aliens, objs_ship, is_fire):
    if param_game.allow_fire:
        param_game.allow_fire = False
        if is_fire:
            missile_position = pygame.Vector2(objs_ship.ship.rect.midtop)
            bullet = obj_game.Missile(param_game.game_board.screen,
                                          missile_position,
                                          objs_aliens.aliens,
                                      param_game.game_board.screen_fields)
            bullet.fire()
            objs_ship.bullets.add(bullet)

def main_in_loop(display, time_struct, ship_objects, aliens_objects,
                 parameters_game):
    step = game_parameters.event_catch()
    fire = MovingType.FIRE in step.type
    ship_fire(game_parameters, game_objects, aliens_objects, ship_objects, fire)
    bomb_fall(aliens_objects.aliens, aliens_objects.bombs, ship_objects.ship,
              display, game_parameters.game_board.screen_fields)
    for obj in aliens_objects.aliens | aliens_objects.bombs:
        obj.move()

    ship_objects.ship.move(step.move if MovingType.MOVE in step.type else 0)
    for bullet in ship_objects.bullets:
        is_hit = bullet.move()
        if is_hit:
            game_parameters.points += 10
    pause_on_hit = False
    for bomb in aliens_objects.bombs:
        if bomb.is_hit():
            parameters_game.live_numb -= 1
            pause_on_hit = True
            break
    aliens_hit = set()
    for alien in aliens_objects.aliens:
        if alien.touch_ship(ship_objects.ship):
            aliens_hit.add(alien)
            parameters_game.live_numb -= 1
            pause_on_hit = True
    aliens_objects.aliens.difference_update(aliens_hit)
    aliens_objects.fall()
    aliens_objects.put_to_start_position()
    display.blit(parameters_game.background, (0, 0))
    for obj in (aliens_objects.aliens | {ship_objects.ship} |
                ship_objects.bullets | aliens_objects.bombs):
        obj.draw()
    show_lives(parameters_game.live_numb, display)
    parameters_game.show_point(display)
    end_bullets = {b for b in ship_objects.bullets if not b.visible}
    ship_objects.bullets.difference_update(end_bullets)
    end_bombs = {bomb for bomb in aliens_objects.bombs if not bomb.visible}
    aliens_objects.bombs.difference_update(end_bombs)
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
    board_numb = 0
    gb = board.GameBoard(alien_on_board)
    while True:
        game_parameters = GameParameters(gb)
        welcome_page(gb.screen)
        timer = TimeStruct()
        ship_items = ShipObjects(gb.screen, gb.screen_fields)
        for alien_brd in alien_on_board:
            print(f'alien-brd = {alien_brd}')
            gb.put_one(alien_brd)
            aliens_atack = AliensObjects(gb.aliens)
            pygame.time.set_timer(ALLOWFIRE, 100)
            while game_parameters.running:
                main_in_loop(gb.screen, timer, ship_items,
                             aliens_atack,
                             game_parameters)
                # if game_parameters.live_numb <= 0:
                #     game_parameters.running = False
                if not aliens_atack.aliens:
                    board_numb = + 1
                    break
                if not game_parameters.running:
                    gameover_page(gb.screen)
    pygame.quit()
