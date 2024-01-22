from os import path
from pathlib import Path
import pygame
from game_objects import Alien

import screen_field


ALIEN_BEGIN = pygame.Vector2(100, 100)
SPACE_BETWEEN_ALIENS = 50
PATH = Path(path.abspath('images')).joinpath('alien1.png')

class GameBoard:
    def __init__(self, str_board_list):
        self.aliens = []
        self._str_board_list = str_board_list
        self._position = pygame.Vector2(ALIEN_BEGIN)
        self.screen_fields = screen_field.ScreenFields()
        resolution = (self.screen_fields.joyfield_size[0] +
                      self.screen_fields.playfield_size[0] +
                      self.screen_fields.firefield_size[0], 480)
        self.screen = pygame.display.set_mode(resolution,
                                              pygame.FULLSCREEN | pygame.SCALED
                                            )
        print(self.screen)

    def put_in_row(self, line):
        self._position.x = ALIEN_BEGIN.x
        for char in line:
            if char == 'x':
                self.aliens.append(Alien(PATH, self.screen, self._position,
                                         self.screen_fields))
            self._position += pygame.Vector2(SPACE_BETWEEN_ALIENS, 0)

    def put_one(self, str_board):
        self._position = pygame.Vector2(ALIEN_BEGIN)
        self.aliens = []
        for line in str_board.splitlines():
            self.put_in_row(line)
            self._position += pygame.Vector2(0, SPACE_BETWEEN_ALIENS)
