from animationstudio.animation import Animation
from animationstudio.events import Events
from animationstudio.events import Observable
from animationstudio.geometry import Size
from animationstudio.graphics import Graphics
from animationstudio.render import VideoRenderer

import pygame

import importlib
import os

class Preview(Observable):

    """
    I run and quit:

    >>> preview = Preview.create_null(
    ...     events=[None, pygame.event.Event(pygame.QUIT)]
    ... ).run(Animation())

    I kick off rendering if 'r' is pressed:

    >>> renderer = VideoRenderer.create_null()
    >>> events = renderer.track_events()
    >>> preview = Preview.create_null(
    ...     events=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)],
    ...     renderer=renderer
    ... )
    >>> preview.run(Animation())
    >>> events # doctest: +ELLIPSIS
    Write =>
        path: '/tmp/frame0001.png'
    ...

    I can create myself:

    >>> isinstance(Preview.create(), Preview)
    True
    """

    @staticmethod
    def create():
        return Preview(
            pygame=pygame,
            graphics=Graphics.create(),
            renderer=VideoRenderer.create(),
            animation_loader=AnimationLoader.create()
        )

    @staticmethod
    def create_null(events=[None, pygame.event.Event(pygame.QUIT)], renderer=VideoRenderer.create_null()):
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
                event = events.pop(0)
                if event:
                    return [event]
                else:
                    return []
        class NullImage:
            def frombuffer(self, buffer, size, mode):
                pass
        class NullDraw:
            def rect(sefl, screen, color, rect):
                pass
        class NullPygame:
            display = NullDisplay()
            time = NullTime()
            event = NullEvent()
            image = NullImage()
            draw = NullDraw()
            def init(self):
                pass
            def quit(self):
                pass
        return Preview(
            pygame=NullPygame(),
            graphics=Graphics.create_null(),
            renderer=renderer,
            animation_loader=AnimationLoader.create_null()
        )

    def __init__(self, pygame, graphics, renderer, animation_loader):
        Observable.__init__(self)
        self.pygame = pygame
        self.graphics = graphics
        self.renderer = renderer
        self.animation_loader = animation_loader

    def run(self, animation=None, reload=None):
        result = self.loop(animation=animation, reload=reload)
        if result.render:
            self.renderer.render(result.animation, destination="/tmp/animation.mp4")

    def loop(self, animation, reload):
        self.pygame.init()
        screen_size = Size(width=700, height=700)
        screen = self.pygame.display.set_mode(screen_size)
        clock = self.pygame.time.Clock()
        if reload:
            animation = self.animation_loader.load(reload)
            animation.dry_run()
        else:
            animation = animation
        animation.reset()
        elapsed_ms = 0
        animation_elapsed_ms = 0
        try:
            while True:
                if reload and self.animation_loader.changed(reload):
                    animation = self.animation_loader.load(reload)
                    animation.reset()
                for event in self.pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise ExitLoop()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        raise ExitLoop(render=True, animation=animation)
                screen.fill("gray")
                scale_factor = animation.get_size().scale_factor(screen_size.scale(0.90))
                preview_size = animation.get_size().scale(scale_factor)
                x, y = screen_size.center(preview_size)
                w, h = preview_size
                self.pygame.draw.rect(screen, "black", (x, y, w, h))
                surface = self.graphics.create_surface(preview_size, scale_factor)
                animation.update(elapsed_ms)
                animation.draw(surface)
                image = self.pygame.image.frombuffer(
                    surface.get_data(),
                    preview_size,
                    "BGRA"
                )
                screen.blit(image, (x, y))
                self.pygame.display.flip()
                elapsed_ms = clock.tick(60)
                animation_elapsed_ms += elapsed_ms
                if animation_elapsed_ms > animation.get_duration_in_ms():
                    animation_elapsed_ms = 0
                    animation.reset()
        except ExitLoop as e:
            return e
        finally:
            self.pygame.quit()

class ExitLoop(Exception):

    def __init__(self, render=False, animation=None):
        Exception.__init__(self)
        self.render = render
        self.animation = animation

class AnimationLoader(Observable):

    """
    >>> loader = AnimationLoader.create()
    >>> events = loader.track_events()
    >>> animation = loader.load("example")
    >>> isinstance(animation, Animation)
    True
    >>> events
    LOAD_ANIMATION_MODULE =>

    >>> animation = AnimationLoader.create_null().load("i_dont_care_module")
    >>> isinstance(animation, Animation)
    True
    """

    @staticmethod
    def create():
        return AnimationLoader(importlib=importlib, os=os)

    @staticmethod
    def create_null():
        class NullModule:
            __file__ = "null_module.py"
            class ExampleAnimation(Animation):
                pass
        class NullImportlib:
            def import_module(self, name):
                return NullModule()
        class NullStat:
            st_mtime = 0
        class NullOs:
            def stat(self, path):
                return NullStat()
        return AnimationLoader(importlib=NullImportlib(), os=NullOs())

    def __init__(self, importlib, os):
        Observable.__init__(self)
        self.importlib = importlib
        self.os = os
        self.animation_module = None

    def load(self, name):
        if self.animation_module is None:
            self.notify("LOAD_ANIMATION_MODULE", {})
            self.animation_module = self.importlib.import_module(name)
            self.stat(name)
        else:
            self.importlib.reload(self.animation_module)
        return self.animation_module.ExampleAnimation()

    def changed(self, name):
        old_modified_time = self.modified_time
        self.stat(name)
        return old_modified_time != self.modified_time

    def stat(self, name):
        try:
            self.modified_time = self.os.stat(self.animation_module.__file__).st_mtime
        except FileNotFoundError:
            # Vim save removes file temporary?
            pass
