from animationstudio.graphics import Graphics
from animationstudio.render import VideoRenderer

import pygame

class Preview:

    """
    >>> isinstance(Preview.create(), Preview)
    True
    """

    @staticmethod
    def create():
        return Preview(
            pygame=pygame,
            graphics=Graphics.create(),
            renderer=VideoRenderer.create()
        )

    @staticmethod
    def create_null():
        class NullScreen:
            def fill(self, color):
                pass
            def blit(self, surface, position):
                pass
        class NullDisplay:
            def set_mode(self, size):
                return NullScreen()
            def flip(self):
                pass
        class NullTime:
            class Clock:
                def tick(self, fps):
                    return int(1000/fps)
        class NullEvent:
            def get(self):
                return [pygame.event.Event(pygame.QUIT)]
        class NullImage:
            def frombuffer(self, buffer, size, mode):
                pass
        class NullPygame:
            display = NullDisplay()
            time = NullTime()
            event = NullEvent()
            image = NullImage()
            def init(self):
                pass
            def quit(self):
                pass
        return Preview(
            pygame=NullPygame(),
            graphics=Graphics.create_null(),
            renderer=VideoRenderer.create_null()
        )

    def __init__(self, pygame, graphics, renderer):
        self.pygame = pygame
        self.graphics = graphics
        self.renderer = renderer

    def run(self, animation):
        self.pygame.init()
        screen = self.pygame.display.set_mode((1280, 720))
        clock = self.pygame.time.Clock()
        running = True
        animation.reset()
        elapsed_ms = 0
        animation_elapsed_ms = 0
        while running:
            for event in self.pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("black")
            surface = self.graphics.create_surface(400, 400)
            animation.update(elapsed_ms)
            animation.draw(surface)

            image = self.pygame.image.frombuffer(surface.get_data(), (400, 400), "BGRA")
            screen.blit(image, (0, 0))

            self.pygame.display.flip()
            elapsed_ms = clock.tick(60)
            animation_elapsed_ms += elapsed_ms
            if animation_elapsed_ms > animation.get_duration_in_ms():
                animation_elapsed_ms = 0
                animation.reset()
        self.pygame.quit()
