from game_objects import Alien
from pathlib import Path
from copy import copy
import pygame

ALIEN_BEGIN = pygame.Vector2(100, 100)
SPACE_BETWEEN_ALIENS = 50
PATH = Path('images').joinpath('alien1.png')

class GameBoard:
    def __init__(self, aliens, str_board, screen, ship):
        self.aliens = aliens
        self.str_board = str_board.splitlines()
        self.position = copy(ALIEN_BEGIN)
        self._count_line = 0
        self.screen = screen
        self.ship = ship
        
    def put_in_row(self, line):
        self.position.x = ALIEN_BEGIN.x
        print(f'aaa {self.position}')
        
        for char in line:
            print(f'ALIEN_BEGIN {ALIEN_BEGIN}')
            print(self.position)
            if char == 'x':
                self.aliens.add(Alien(PATH, self.screen, self.position, self.ship))
            self.position += pygame.Vector2(SPACE_BETWEEN_ALIENS, 0)               
    def put(self):
        for line in self.str_board:
            self.put_in_row(line)
            self.position += pygame.Vector2(0, SPACE_BETWEEN_ALIENS)
