from  pathlib import Path
import random

import pygame

random.seed()


class Ship():
    def __init__(self, screen):
        path = Path('images')
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        print(screen_width, screen_height)
        self.rect = pygame.Rect(screen_width//2, screen_height-20, 20, 20)
        self.speed = pygame.Vector2(1, 0)
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

    def move(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect = self.rect.move(-self.speed)
            self.current_frame = self.ships['left']
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect = self.rect.move(self.speed)
            self.current_frame = self.ships['right']
        else:
            self.current_frame = self.ships['straight']
        right_pos = self.rect.right
        left_pos = self.rect.left
        rect_screen = self.screen.get_rect()
        if right_pos >= rect_screen.right:
            self.rect = self.rect.move(rect_screen.right - right_pos, 0)
        if left_pos <= rect_screen.left:
            self.rect = self.rect.move(rect_screen.left - left_pos, 0)


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

    def move(self):
        if self.visible:
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
        self.is_hit()

    def is_hit(self):
        ship = self.ship
        if self.rect.colliderect(ship.rect):
            pygame.quit()
            exit()

    def fire(self):
        self.visible = True

    def draw(self):
        if self.visible:
            self.screen.blit(self.current_frame, self.rect)



class Alien():
    possible_move = 20
    def __init__(self, path, screen, position, ship):
        self.screen = screen
        self.current_frame = pygame.image.load(path)
        self.rect = self.current_frame.get_rect()
        self.rect.move_ip(position)
        self.initial_rect = pygame.Rect(self.rect)
        self.speed = pygame.Vector2(random.choice((-1, 1)), 0)
        self.fallen_speed = pygame.Vector2(2, 1)
        self.show = True
        self.is_fallen = False
        self.is_out = False
        self.ship = ship

    def fallen(self): 
        if random.randint(1, 10000) == 6:
            self.is_fallen = True
            self.speed = self.fallen_speed

    def alien_is_out(self):
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
                self.speed = pygame.Vector2(-self.speed.x, self.speed.y)
        else:
            self.rect.move_ip(self.speed)
            if (self.rect.right >= self.initial_rect.x + self.possible_move or
                self.rect.left <= self.initial_rect.x - self.possible_move):
                self.speed = -self.speed
        self.touch_ship()

    def touch_ship(self):
        if self.rect.colliderect(self.ship.rect):
            pygame.quit()
            exit()


    def draw(self):
        self.screen.blit(self.current_frame, self.rect)
