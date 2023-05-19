from animations.test import TestAnimation
from graphics import Graphics

import pygame

class Preview:

    """
    >>> Preview.create_null().run(TestAnimation())
    Reset
    FillRect =>
      x: 10

    >>> isinstance(Preview.create(), Preview)
    True
    """

    @staticmethod
    def create():
        return Preview(pygame=pygame, graphics=Graphics.create())

    @staticmethod
    def create_null():
        class NullScreen:
            def fill(self, color):
                pass
        class NullDisplay:
            def set_mode(self, size):
                return NullScreen()
            def flip(self):
                pass
        class NullTime:
            class Clock:
                def tick(self, fps):
                    pass
        class NullEvent:
            def get(self):
                return [pygame.event.Event(pygame.QUIT)]
        class NullPygame:
            display = NullDisplay()
            time = NullTime()
            event = NullEvent()
            def init(self):
                pass
            def quit(self):
                pass
        return Preview(pygame=NullPygame(), graphics=Graphics.create_null())

    def __init__(self, pygame, graphics):
        self.pygame = pygame
        self.graphics = graphics

    def run(self, animation):
        self.pygame.init()
        screen = self.pygame.display.set_mode((1280, 720))
        clock = self.pygame.time.Clock()
        running = True
        animation.reset()
        while running:
            for event in self.pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("purple")
            surface = self.graphics.create_surface(400, 400)
            animation.draw(surface)
            self.pygame.display.flip()
            clock.tick(60)
        self.pygame.quit()
