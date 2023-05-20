from animationstudio import *

class ExampleAnimation(Animation):

    """
    >>> ExampleAnimation().dry_run() # doctest: +ELLIPSIS
    Write /tmp/frame0001.png
    ...
    Write /tmp/frame0075.png
    """

    def get_size(self):
        return Size(width=1920, height=1080)

    def get_duration_in_ms(self):
        return 3000

    def reset(self):
        self.x = 10

    def update(self, elapsed_ms):
        self.x += elapsed_ms*0.1

    def draw(self, surface):
        surface.fill_rect(self.x, 10, 10, 10, color=(0.1, 0.5, 0.8))
