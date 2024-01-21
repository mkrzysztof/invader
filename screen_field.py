import pygame

class ScreenFields:
    def __init__(self):
        self.joyfield_size = pygame.Vector2(80, 480)
        self.playfield_size = pygame.Vector2(640, 480)
        self.firefield_size = pygame.Vector2(20, 480)
        self.__init_begin_rect()

    def __init_begin_rect(self):
        begin = pygame.Vector2(0, 0)
        self.joyfield = pygame.Rect(begin, self.joyfield_size)
        begin = pygame.Vector2(begin.x + self.joyfield_size.x + 1, 0)
        self.playfield = pygame.Rect(begin, self.playfield_size)
        begin = pygame.Vector2(begin.x + self.playfield_size.x, 0)
        self.firefield = pygame.Rect(begin, self.firefield_size)
        print(self.joyfield, self.playfield, self.firefield)