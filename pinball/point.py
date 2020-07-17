import pygame

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pass

    def int(self):
        return int(self.x), int(self.y)