from animationstudio.geometry import Point
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
                def stroke(self):
                    pass
                def save(self):
                    pass
                def restore(self):
                    pass
                def scale(self, x_factor, y_factor):
                    pass
                def move_to(self, x, y):
                    pass
                def translate(self, x, y):
                    pass
                def rotate(self, amount):
                    pass
                def text_path(self, text):
                    pass
                def set_font_size(self, size):
                    pass
                def text_extents(self, text):
                    return Size(100, 100)
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
    >>> s.fill_rect(0, 0, 10, 10, color=(0.5, 1, 0.3))
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

    def fill_rect(self, x, y, width, height, **kwargs):
        print("FillRect =>")
        print(f"  x: {x}")
        with self.ctx() as ctx:
            ctx.rectangle(x, y, width, height)
            self.apply_generic_attributes(ctx, **kwargs)
            ctx.fill()

    def text(self, text, position, pointspec="center", **kwargs):
        with self.ctx() as ctx:
            ctx.set_font_size(500)
            ctx.translate(position.x, position.y)
            self.apply_generic_attributes(ctx, **kwargs)
            extents = ctx.text_extents(text)
            position = Point(0, 0).adjust(
                Size(width=extents.width, height=extents.height),
                pointspec
            ).move(dy=extents.height)
            ctx.translate(position.x, position.y)
            ctx.text_path(text)
            ctx.fill()
            ctx.text_path(text)
            ctx.set_source_rgb(0.2, 1, 1)
            ctx.stroke()

    def apply_generic_attributes(self, ctx, **kwargs):
        if "scale" in kwargs:
            ctx.scale(kwargs["scale"], kwargs["scale"])
        if "color" in kwargs:
            ctx.set_source_rgb(*kwargs["color"])
        if "rotation" in kwargs:
            ctx.rotate(kwargs["rotation"])

    def write_to_file(self, destination):
        print(f"Write {destination}")
        self.surface.write_to_png(destination)

    def get_data(self):
        return self.surface.get_data()
