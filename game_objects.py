from os import path
from  pathlib import Path
import random

import pygame
from pygame._sdl2 import touch

random.seed()


class Ship():
    def __init__(self, screen):
        pth = Path(path.abspath('images'))
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.rect = pygame.Rect(screen_width//2, screen_height-20, 20, 20)
        self.speed = pygame.Vector2(1, 0)
        self.screen = screen
        self.ships = {}
        ship_path = pth.joinpath('ship_straight.png')
        self.ships['straight'] = pygame.image.load(ship_path)
        ship_path = pth.joinpath('ship_left.png')
        self.ships['left'] = pygame.image.load(ship_path)
        ship_path = pth.joinpath('ship_right.png')
        self.ships['right'] = pygame.image.load(ship_path)
        self.current_frame = self.ships['straight']
        boom_path = pth.joinpath('boom.png')
        self.boom = pygame.image.load(boom_path)
        self.allow_move = False
        self.pos = self.rect.topleft[0]

    def draw(self):
        self.screen.blit(self.current_frame, self.rect)

    def move(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect = self.rect.move(-self.speed)
            self.current_frame = self.ships['left']
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect = self.rect.move(self.speed)
            self.current_frame = self.ships['right']
        else:
            self.current_frame = self.ships['straight']
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                print(event)
                relative = event.pos[0] - self.pos
                absrel = abs(relative)
                if relative < 0:
                    self.rect = self.rect.move(-absrel * self.speed)
                    self.current_frame = self.ships['left']
                elif relative > 0:
                    self.rect = self.rect.move(absrel * self.speed)
                    self.current_frame = self.ships['right']
                else:
                    self.current_frame = self.ships['straight']
                self.pos = event.pos[0]
            else:
                pygame.event.post(event)
        right_pos = self.rect.right
        left_pos = self.rect.left
        rect_screen = self.screen.get_rect()
        if right_pos >= rect_screen.right:
            self.rect = self.rect.move(rect_screen.right - right_pos, 0)
        if left_pos <= rect_screen.left:
            self.rect = self.rect.move(rect_screen.left - left_pos, 0)


class Missile():
    current_frame = pygame.image.load(
            Path(path.abspath('images')).joinpath('missile.png'))
    def __init__(self, screen, position, aliens):
        self.rect = self.current_frame.get_rect()
        self.rect.move_ip(position)
        self.speed = pygame.Vector2(0, -3)
        self.screen = screen
        self.visible = False
        self.aliens = aliens

    def move(self):
        if self.visible:
            self.rect.move_ip(self.speed)
        if self.rect.midbottom[1] <= 0:
            self.visible = False
        hit = self.is_hit()
        return hit


    def draw(self):
        if self.visible:
            self.screen.blit(self.current_frame, self.rect)

    def fire(self):
        self.visible = True

    def is_hit(self):
        al_del = None
        for al in self.aliens:
            if al.rect.colliderect(self.rect):
                self.visible = False
                al.show = False
                al_del = al
        if al_del:
            self.aliens.remove(al_del)
            return True
        return False

class Bomb():
    current_frame = pygame.image.load(
            Path(path.abspath('images')).joinpath('missile.png'))
    def __init__(self, screen, alien, ship):
        self.rect = self.current_frame.get_rect()
        self.rect.move_ip(alien.rect.midbottom)
        self.visible = False
        self.speed = pygame.Vector2(0, 3)
        self.ship = ship
        self.screen = screen

    def move(self):
        self.rect.move_ip(self.speed)
        if not self.screen.get_rect().contains(self.rect):
            self.visible = False

    def is_hit(self):
        ship = self.ship
        if self.rect.colliderect(ship.rect):
            self.visible = False
            self.ship.current_frame = self.ship.boom
            return True
        return False

    def fire(self):
        self.visible = True

    def draw(self):
        if self.visible:
            self.screen.blit(self.current_frame, self.rect)



class Alien():
    possible_move = 20
    def __init__(self, img_path, screen, position):
        self.screen = screen
        self.current_frame = pygame.image.load(img_path)
        self.rect = self.current_frame.get_rect()
        self.rect.move_ip(position)
        self.initial_rect = pygame.Rect(self.rect)
        self.speed = pygame.Vector2(random.choice((-1, 1)), 0)
        self.fallen_speed = pygame.Vector2(2, 1)
        self.show = True
        self.is_fallen = False
        self.is_out = False

    def fallen(self):
        if random.randint(1, 1000) == 6:
            self.is_fallen = True
            self.speed = self.fallen_speed

    def put_to_start_pos(self):
        if self.rect.topleft[1] >= self.screen.get_height():
            self.is_out = True
            self.rect = pygame.Rect(self.initial_rect)
            self.is_fallen = False
            self.speed = pygame.Vector2(self.speed.x, 0)

    def move(self):
        if self.is_fallen:
            self.rect.move_ip(self.speed)
            if (self.rect.left <= 0
                or self.rect.right > self.screen.get_width()):
                self.speed = pygame.Vector2(0-self.speed.x, self.speed.y)
        else:
            self.rect.move_ip(self.speed)
            if (self.rect.right >= self.initial_rect.x + self.possible_move or
                self.rect.left <= self.initial_rect.x - self.possible_move):
                self.speed = -self.speed

    def touch_ship(self, ship):
        if self.rect.colliderect(ship.rect):
            ship.current_frame = ship.boom
            return True
        return False

    def draw(self):
        self.screen.blit(self.current_frame, self.rect)
