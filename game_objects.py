from  pathlib import Path
import random

import pygame
import pygame.math as pymath

random.seed()

ALIENMOVE = pygame.event.custom_type()
MISSILLEMOVE = pygame.event.custom_type()
SHIPMOVE = pygame.event.custom_type()


class Ship():
    def __init__(self, screen):
        path = Path('images')
        self.ships = {}
        ship_path = path.joinpath('ship_straight.png')
        self.ships['straight'] = pygame.image.load(ship_path)
        ship_path = path.joinpath('ship_left.png')
        self.ships['left'] = pygame.image.load(ship_path)
        ship_path = path.joinpath('ship_right.png')
        self.ships['right'] = pygame.image.load(ship_path)
        self.screen = screen
        self.delta = pymath.Vector2(4, 0)
        self.posx = 200
        self.posy = 500
        self.position = pymath.Vector2(200, 500)
        self.current_frame = self.ships['straight']
        self.allow_move = False
        
    def draw(self):
        pygame.Surface.blit(self.screen, self.current_frame, self.position)

    def move(self, event):
        if event.type == SHIPMOVE:
            self.allow_move = True
        if event.type == pygame.KEYDOWN and self.allow_move:
            if event.key == pygame.K_LEFT:
                self.position -= self.delta
                self.current_frame = self.ships['left']
                self.allow_move = False
            if event.key == pygame.K_RIGHT:
                self.position += self.delta
                self.current_frame = self.ships['right']
                self.allow_move = False
        else:
            self.current_frame = self.ships['straight']


class Missile():
    speed = 1
    current_frame = pygame.image.load(
            Path('images').joinpath('missile.png'))
    def __init__(self, screen, ship, aliens):
        self.ship = ship
        self.screen = screen
        self.bang = False
        self.tick = 0
        self._dy = 3
        self.aliens = aliens
        self.position = self.ship.position + pymath.Vector2(8, 0)

    def move(self, event):
        if self.bang:
            if event.type == MISSILLEMOVE:
                self.position += pymath.Vector2(0, -3)
        if self.position.y <= 0:
            self.bang = False
        self.is_hit()
            

    def draw(self):
        if self.bang:
            pygame.Surface.blit(self.screen, self.current_frame,
                                self.position)

    def fire(self):
        self.bang = True

    def is_hit(self):
        rect_miss = self.current_frame.get_rect()
        rect_miss = rect_miss.move(self.position)
        for al in self.aliens:
            rect_al = al.current_frame.get_rect()
            rect_al = rect_al.move(al.posx, al.posy)
            if rect_al.colliderect(rect_miss):
                self.bang = False
                al.show = False
                print("bang")
        al_del = {al for al in self.aliens if not al.show}
        for al in al_del:
            self.aliens.remove(al)

class Bomb():
    def __init__(self, screen, position):
        pass


class Alien():
    def __init__(self, path, screen, position):
        self.screen = screen
        self.current_frame = pygame.image.load(path)
        self.position = position
        self._position = position
        self.show = True
        self.delta = pymath.Vector2(random.choice((-2, 2, -3, 3, -4, 4)), 0)

    def move(self, event):
        print(f'{id(self)} , {self.delta}')
        pos_start = self._position
        if event.type == ALIENMOVE:
            self.position += self.delta
            if self.position.x >= pos_start.x + 10 or self.position.x <= pos_start.x - 10:
                self.delta = -self.delta

    def draw(self):
        pygame.Surface.blit(self.screen, self.current_frame, self.position)
    
