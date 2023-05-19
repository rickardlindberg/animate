from animationstudio.geometry import Size

import cairo

import contextlib

class Graphics:

    @staticmethod
    def create():
        return Graphics(cairo)

    @staticmethod
    def create_null():
        class NullCairoModule:
            FORMAT_ARGB32 = object()
            class NullContext:
                def __init__(self, surface):
                    pass
                def rectangle(self, x, y, width, heigt):
                    pass
                def set_source_rgb(self, r, g, b):
                    pass
                def fill(self):
                    pass
                def save(self):
                    pass
                def restore(self):
                    pass
                def scale(self, x_factor, y_factor):
                    pass
                def move_to(self, x, y):
                    pass
                def show_text(self, text):
                    pass
                def set_font_size(self, size):
                    pass
            Context = NullContext
            class NullImageSurface:
                def __init__(self, format_, width, height):
                    pass
                def write_to_png(self, destination):
                    pass
                def get_data(self):
                    pass
            ImageSurface = NullImageSurface
        return Graphics(NullCairoModule())

    def __init__(self, cairo):
        self.cairo = cairo

    def create_surface(self, size, scale_factor=1):
        return CairoSurfaceWrapper(self.cairo, size, scale_factor)

class CairoSurfaceWrapper:

    """
    >>> s = CairoSurfaceWrapper(cairo, Size(width=400, height=400), 1)
    >>> s.fill_rect(0, 0, 10, 10, (0.5, 1, 0.3))
    FillRect =>
      x: 0
    """

    def __init__(self, cairo, size, scale_factor):
        self.cairo = cairo
        self.surface = self.cairo.ImageSurface(
            self.cairo.FORMAT_ARGB32,
            size.width,
            size.height
        )
        self.scale_factor = scale_factor

    @contextlib.contextmanager
    def ctx(self):
        ctx = self.cairo.Context(self.surface)
        ctx.save()
        try:
            ctx.scale(self.scale_factor, self.scale_factor)
            yield ctx
        finally:
            ctx.restore()

    def fill_rect(self, x, y, width, height, color):
        print("FillRect =>")
        print(f"  x: {x}")
        with self.ctx() as ctx:
            ctx.rectangle(x, y, width, height)
            ctx.set_source_rgb(*color)
            ctx.fill()

    def text(self, text, position):
        with self.ctx() as ctx:
            ctx.set_source_rgb(1, 1, 1)
            ctx.set_font_size(200)
            ctx.move_to(position.x, position.y)
            ctx.show_text(text)

    def write_to_file(self, destination):
        print(f"Write {destination}")
        self.surface.write_to_png(destination)

    def get_data(self):
        return self.surface.get_data()
