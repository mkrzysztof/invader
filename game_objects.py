from  pathlib import Path
import random

import pygame

random.seed()

ALIENMOVE = pygame.event.custom_type()
MISSILLEMOVE = pygame.event.custom_type()
SHIPMOVE = pygame.event.custom_type()
BOMBMOVE = pygame.event.custom_type()


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
        self.delta = pygame.Vector2(4, 0)
        self.position = pygame.Vector2(200, 500)
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
        self.visible = False
        self.tick = 0
        self._dy = 3
        self.aliens = aliens
        self.position = self.ship.position + pygame.Vector2(8, 0)

    def move(self, event):
        if self.visible:
            if event.type == MISSILLEMOVE:
                self.position += pygame.Vector2(0, -3)
        if self.position.y <= 0:
            self.visible = False
        self.is_hit()
            

    def draw(self):
        if self.visible:
            pygame.Surface.blit(self.screen, self.current_frame,
                                self.position)

    def fire(self):
        self.visible = True

    def is_hit(self):
        rect_miss = self.current_frame.get_rect()
        rect_miss = rect_miss.move(self.position)
        for al in self.aliens:
            rect_al = al.current_frame.get_rect()
            rect_al = rect_al.move(al.position)
            if rect_al.colliderect(rect_miss):
                self.visible = False
                al.show = False
        al_del = {al for al in self.aliens if not al.show}
        for al in al_del:
            self.aliens.remove(al)

class Bomb():
    current_frame = pygame.image.load(
            Path('images').joinpath('missile.png'))
    def __init__(self, screen, alien):
        self.position = alien.position + pygame.Vector2(0, 20)
        self.visible = False
        self.delta = pygame.Vector2(0, 3)
        self.screen = screen

    def move(self, event):
        if self.visible and event.type == BOMBMOVE:
            self.position += self.delta
        if self.position.y >= self.screen.get_height():
            self.visible = False
        self.is_hit()

    def is_hit(self):
        pass

    def fire(self):
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.Surface.blit(self.screen, self.current_frame,
                                self.position)
        


class Alien():
    def __init__(self, path, screen, position):
        self.screen = screen
        self.current_frame = pygame.image.load(path)
        self.position = position
        self._position = pygame.Vector2(position)
        self.show = True
        self.delta = pygame.Vector2(random.choice((-2, 2, -3, 3, -4, 4)), 0)

    def move(self, event):
        pos_start = self._position
        if event.type == ALIENMOVE:
            self.position += self.delta
            if self.position.x >= pos_start.x + 10 or self.position.x <= pos_start.x - 10:
                self.delta = -self.delta

    def draw(self):
        pygame.Surface.blit(self.screen, self.current_frame, self.position)
    
