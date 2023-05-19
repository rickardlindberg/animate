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
            width=self.width*factor,
            height=self.height*factor
        )

class Point(namedtuple("Pint", "x,y")):
    pass
