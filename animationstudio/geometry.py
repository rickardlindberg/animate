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

class Point(namedtuple("Pint", "x,y")):
    pass
