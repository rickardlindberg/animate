import cairo

class Graphics:

    @staticmethod
    def create():
        return Graphics(cairo)

    @staticmethod
    def create_null():
        class NullCairoModule:
            FORMAT_ARGB32 = object()
            class ImageSurface:
                def __init__(self, format_, width, height):
                    pass
                def write_to_png(self, destination):
                    pass
            class Context:
                def __init__(self, surface):
                    pass
                def rectangle(self, x, y, width, heigt):
                    pass
                def set_source_rgb(self, r, g, b):
                    pass
                def fill(self):
                    pass
        return Graphics(NullCairoModule())

    def __init__(self, cairo):
        self.cairo = cairo

    def create_surface(self, width, height):
        return CairoSurfaceWrapper(self.cairo, width, height)

class CairoSurfaceWrapper:

    """
    >>> s = CairoSurfaceWrapper(cairo, 400, 400)
    >>> s.fill_rect(0, 0, 10, 10, (0.5, 1, 0.3))
    FillRect =>
      x: 0
    """

    def __init__(self, cairo, width, height):
        self.cairo = cairo
        self.surface = self.cairo.ImageSurface(self.cairo.FORMAT_ARGB32, width, height)

    def fill_rect(self, x, y, width, height, color):
        print("FillRect =>")
        print(f"  x: {x}")
        ctx = self.cairo.Context(self.surface)
        ctx.rectangle(x, y, width, height)
        ctx.set_source_rgb(*color)
        ctx.fill()

    def write_to_file(self, destination):
        print(f"Write {destination}")
        self.surface.write_to_png(destination)
