from animationstudio.events import Observable
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
                def fill_preserve(self):
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
                def set_line_width(self, width):
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
                    class E:
                        x_bearing = 0
                        y_bearing = 0
                        width = 100
                        height = 100
                    return E()
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

class CairoSurfaceWrapper(Observable):

    """
    >>> s = CairoSurfaceWrapper(cairo, Size(width=400, height=400), 1)
    >>> events = s.track_events()
    >>> s.fill_rect(0, 0, 10, 10, color=(0.5, 1, 0.3))
    >>> events
    FillRect =>
        x: 0
    """

    def __init__(self, cairo, size, scale_factor):
        Observable.__init__(self)
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

    def fill_rect(self, x, y, width, height, pointspec="center", **kwargs):
        self.notify("FillRect", {"x": x})
        with self.ctx() as ctx:
            self.apply_generic_attributes(ctx, **kwargs)
            position = Point(x, y).adjust(
                Size(width=width, height=height),
                pointspec
            )
            ctx.rectangle(*position, width, height)
            self.fill_stroke(ctx, **kwargs)

    def text_size(self, text, **kwargs):
        with self.ctx() as ctx:
            self.apply_generic_attributes(ctx, **kwargs)
            return ctx.text_extents(text)

    def text(self, text, position, pointspec="center", **kwargs):
        extents = self.text_size(text, **kwargs)
        with self.ctx() as ctx:
            ctx.translate(position.x, position.y)
            self.apply_generic_attributes(ctx, **kwargs)
            position = Point(0, 0).adjust(
                Size(width=extents.width, height=extents.height),
                pointspec
            ).move(dx=-extents.x_bearing, dy=-extents.y_bearing)
            ctx.translate(position.x, position.y)
            ctx.text_path(text)
            self.fill_stroke(ctx, **kwargs)

    def fill_stroke(self, ctx, **kwargs):
        if "color" in kwargs:
            ctx.set_source_rgb(*kwargs["color"])
        ctx.fill_preserve()
        if "stroke_color" in kwargs:
            ctx.set_source_rgb(*kwargs["stroke_color"])
        ctx.set_line_width(15)
        ctx.stroke()

    def apply_generic_attributes(self, ctx, **kwargs):
        if "scale" in kwargs:
            ctx.scale(kwargs["scale"], kwargs["scale"])
        if "rotation" in kwargs:
            ctx.rotate(kwargs["rotation"])
        ctx.set_font_size(kwargs.get("font_size", 250))

    def write_to_file(self, destination):
        self.surface.write_to_png(destination)

    def get_data(self):
        return self.surface.get_data()
