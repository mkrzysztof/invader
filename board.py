from copy import copy
from os import path
from pathlib import Path
import pygame
from game_objects import Alien


ALIEN_BEGIN = pygame.Vector2(100, 100)
SPACE_BETWEEN_ALIENS = 50
PATH = Path(path.abspath('images')).joinpath('alien1.png')

class GameBoard:
    def __init__(self, aliens, str_board, screen):
        self.aliens = aliens
        self.str_board = str_board.splitlines()
        self.position = copy(ALIEN_BEGIN)
        self.screen = screen

    def put_in_row(self, line):
        self.position.x = ALIEN_BEGIN.x
        for char in line:
            if char == 'x':
                self.aliens.add(Alien(PATH, self.screen, self.position))
            self.position += pygame.Vector2(SPACE_BETWEEN_ALIENS, 0)

    def put(self):
        for line in self.str_board:
            self.put_in_row(line)
            self.position += pygame.Vector2(0, SPACE_BETWEEN_ALIENS)
