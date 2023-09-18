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
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        print(screen_width, screen_height)
        self.rect = pygame.Rect(screen_width//2, screen_height-20, 20, 20)
        self.speed = pygame.Vector2(4, 0)
        self.screen = screen
        self.ships = {}
        ship_path = path.joinpath('ship_straight.png')
        self.ships['straight'] = pygame.image.load(ship_path)
        ship_path = path.joinpath('ship_left.png')
        self.ships['left'] = pygame.image.load(ship_path)
        ship_path = path.joinpath('ship_right.png')
        self.ships['right'] = pygame.image.load(ship_path)
        self.current_frame = self.ships['straight']
        self.allow_move = False

    def draw(self):
        self.screen.blit(self.current_frame, self.rect)

    def move(self, event):
        if event.type == SHIPMOVE:
            self.allow_move = True
        if event.type == pygame.KEYDOWN and self.allow_move:
            if event.key == pygame.K_LEFT:
                speed = -self.speed
                self.rect = self.rect.move(speed)
                self.current_frame = self.ships['left']
                self.allow_move = False
            if event.key == pygame.K_RIGHT:
                speed = self.speed
                self.rect = self.rect.move(speed)
                self.current_frame = self.ships['right']
                self.allow_move = False
        else:
            self.current_frame = self.ships['straight']


class Missile():
    current_frame = pygame.image.load(
            Path('images').joinpath('missile.png'))
    def __init__(self, screen, ship, aliens):
        position = pygame.Vector2(ship.rect.midtop)
        self.rect = self.current_frame.get_rect()
        self.rect.move_ip(position)
        self.speed = pygame.Vector2(0, -3)
        self.ship = ship
        self.screen = screen
        self.visible = False
        self.aliens = aliens

    def move(self, event):
        if self.visible:
            if event.type == MISSILLEMOVE:
                # self.position += self.speed
                self.rect.move_ip(self.speed)
        if self.rect.midbottom[1] <= 0:
            self.visible = False
        self.is_hit()


    def draw(self):
        if self.visible:
            self.screen.blit(self.current_frame, self.rect)

    def fire(self):
        self.visible = True

    def is_hit(self):
        for al in self.aliens:
            if al.rect.colliderect(self.rect):
                self.visible = False
                al.show = False
        al_del = {al for al in self.aliens if not al.show}
        for al in al_del:
            self.aliens.remove(al)

class Bomb():
    current_frame = pygame.image.load(
            Path('images').joinpath('missile.png'))
    def __init__(self, screen, alien, ship):
        self.position = alien.position + pygame.Vector2(0, 20)
        self.visible = False
        self.delta = pygame.Vector2(0, 3)
        self.ship = ship
        self.screen = screen

    def move(self, event):
        if self.visible and event.type == BOMBMOVE:
            self.position += self.delta
        if self.position.y >= self.screen.get_height():
            self.visible = False
        self.is_hit()

    def is_hit(self):
        ship = self.ship
        rect_bomb = self.current_frame.get_rect()
        rect_bomb = rect_bomb.move(self.position)
        if rect_bomb.colliderect(ship.rect):
            pygame.quit()
            exit()

    def fire(self):
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.Surface.blit(self.screen, self.current_frame,
                                self.position)



class Alien():
    possible_move = 10
    def __init__(self, path, screen, position):
        self.screen = screen
        self.position = position
        self.current_frame = pygame.image.load(path)
        self.rect = self.current_frame.get_rect()
        self.rect.move_ip(self.position)
        self.initial_rect = pygame.Rect(self.rect)
        self.speed = pygame.Vector2(random.choice((-2, 2, -3, 3, -4, 4)), 0)
        self.fallen_speed = pygame.Vector2(2, 1)
        self.show = True
        self.is_fallen = False
        self.is_out = False

    def fallen(self):
        r = random.randint(1, 10000)
        if  r == 6:
            self.is_fallen = True
            self.speed = self.fallen_speed

    def alien_is_out(self):
        if self.rect.topleft[1] >= self.screen.get_height():
            self.is_out = True
            self.rect = pygame.Rect(self.initial_rect)
            self.is_fallen = False
            self.speed = pygame.Vector2(self.speed.x, 0)
        

    def move(self, event):
        if event.type == ALIENMOVE:
            # self.position += self.speed
            if self.is_fallen:
                self.rect.move_ip(self.speed)
                if (self.rect.topleft[0] <= 0
                    or self.rect.topright[0] > self.screen.get_width()):
                    self.speed = pygame.Vector2(-self.speed.x, self.speed.y)
            else:
                self.rect.move_ip(self.speed)
                if (self.rect.topleft[0] >= self.position.x + self.possible_move or
                    self.rect.topleft[0] <= self.position.x - self.possible_move):
                    self.speed = -self.speed


    def draw(self):
        self.screen.blit(self.current_frame, self.rect)
