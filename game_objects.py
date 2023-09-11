from  pathlib import Path
import random

import pygame

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
        self._dx = 8
        self.posx = 200
        self.posy = 500
        self.current_frame = self.ships['straight']
        self.allow_move = False
        
    def draw(self):
        pygame.Surface.blit(self.screen, self.current_frame, (self.posx, self.posy))

    def move(self, event):
        if event.type == SHIPMOVE:
            self.allow_move = True
        if event.type == pygame.KEYDOWN and self.allow_move:
            if event.key == pygame.K_LEFT:
                self.posx -= self._dx
                self.current_frame = self.ships['left']
                self.allow_move = False
            if event.key == pygame.K_RIGHT:
                self.posx += self._dx
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

    def move(self, event):
        if self.bang:
            if event.type == MISSILLEMOVE:
                self.posy -= self._dy
        if self.posy <= 0:
            self.bang = False
        self.is_hit()
            

    def draw(self):
        if self.bang:
            pygame.Surface.blit(self.screen, self.current_frame,
                                (self.posx, self.posy))

    def fire(self):
        self.posx = self.ship.posx + 8
        self.posy = self.ship.posy
        self.bang = True

    def is_hit(self):
        rect_miss = self.current_frame.get_rect()
        rect_miss = rect_miss.move(self.posx, self.posy)
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


class Alien():
    def __init__(self, path, screen, position):
        self.screen = screen
        self.current_frame = pygame.image.load(path)
        self.posx, self.posy = position
        self._position = position
        self.show = True
        self.dx = random.choice((-2, 2, -3, 3, -4, 4))

    def move(self, event):
        pos_x_start, _ = self._position
        if event.type == ALIENMOVE:
            self.posx += self.dx
            if self.posx >= pos_x_start + 10 or self.posx <= pos_x_start - 10:
                self.dx = -self.dx

    def draw(self):
        pygame.Surface.blit(self.screen, self.current_frame, (self.posx, self.posy))
    
