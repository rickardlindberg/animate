from animations.test import TestAnimation

import pygame

class Preview:

    """
    >>> Preview.create().run(TestAnimation())

    >>> isinstance(Preview.create(), Preview)
    True
    """

    @staticmethod
    def create():
        return Preview(pygame=pygame)

    @staticmethod
    def create_null():
        return Preview(pygame=NullPygame())

    def __init__(self, pygame):
        self.pygame = pygame

    def run(self, animation):
        self.pygame.init()
        screen = self.pygame.display.set_mode((1280, 720))
        clock = self.pygame.time.Clock()
        running = True
        while running:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
            screen.fill("purple")
            self.pygame.display.flip()
            clock.tick(60)
        self.pygame.quit()
