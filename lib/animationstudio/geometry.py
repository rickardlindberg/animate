from collections import namedtuple

class Size(namedtuple("Size", "width,height")):

    def center(self, size):
        """
        >>> Size(400, 400).center(Size(200, 200))
        Point(x=100, y=100)
        """
        return Point(
            x=(self.width-size.width)//2,
            y=(self.height-size.height)//2,
        )

    def scale_factor(self, size):
        """
        >>> Size(200, 200).scale_factor(Size(400, 400))
        2.0
        """
        width_scale_factor = size.width / self.width
        height_scale_factor = size.height / self.height
        return min(width_scale_factor, height_scale_factor)

    def scale(self, factor):
        """
        >>> Size(100, 100).scale(2)
        Size(width=200, height=200)
        """
        return Size(
            width=int(self.width*factor),
            height=int(self.height*factor)
        )

class Point(namedtuple("Pint", "x,y")):

    def move(self, dx=0, dy=0):
        """
        >>> Point(0, 0).move(1, 2)
        Point(x=1, y=2)
        """
        return Point(x=self.x+dx, y=self.y+dy)

    def adjust(self, size, pointspec):
        """
        >>> p = Point(0, 0)

        >>> p.adjust(Size(100, 100), "topleft")
        Point(x=0, y=0)

        >>> p.adjust(Size(100, 100), "center")
        Point(x=-50, y=-50)

        >>> p.adjust(Size(100, 100), "unknown spec")
        Traceback (most recent call last):
          ...
        ValueError: Unknown pointspec 'unknown spec'.
        """
        if pointspec == "center":
            return self.move(dx=-size.width//2, dy=-size.height//2)
        elif pointspec == "topleft":
            return self
        else:
            raise ValueError(f"Unknown pointspec {pointspec!r}.")
