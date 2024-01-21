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
        self.position = pygame.Vector2(ALIEN_BEGIN)
        self._joyfield_size = (50, 480)
        self._playfield_size = (640, 480)
        self._firefield_size = (50, 480)
        self.screen_fields = screen_field.ScreenFields()
        begin = (0, 0)
        self.joyfield = pygame.Rect(begin, self.screen_fields.joyfield_size)
        begin = (begin[0] + self.screen_fields.joyfield_size[0] + 1, begin[1])
        self.playfield = pygame.Rect(begin, self.screen_fields.playfield_size)
        begin = (begin[0] + self.screen_fields.playfield_size[0] + 1, begin[1])
        self.firefield = pygame.Rect(begin, self.screen_fields.joyfield_size)
        resolution = (self.screen_fields.joyfield_size[0] +
                      self.screen_fields.playfield_size[0] +
                      self.screen_fields.firefield_size[0], 480)
        self.screen = pygame.display.set_mode(resolution,
                                              pygame.FULLSCREEN | pygame.SCALED
                                            )
        print(self.screen)

    def put_in_row(self, line):
        self.position.x = ALIEN_BEGIN.x
        for char in line:
            if char == 'x':
                self.aliens.append(Alien(PATH, self.screen, self.position,
                                         self.screen_fields))
            self.position += pygame.Vector2(SPACE_BETWEEN_ALIENS, 0)

    def put_one(self, str_board):
        self.position = pygame.Vector2(ALIEN_BEGIN)
        self.aliens = []
        for line in str_board.splitlines():
            self.put_in_row(line)
            self.position += pygame.Vector2(0, SPACE_BETWEEN_ALIENS)
