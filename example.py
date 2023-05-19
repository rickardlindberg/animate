from animationstudio import *

class ExampleAnimation(Animation):

    """
    >>> ExampleAnimation().dry_run() # doctest: +ELLIPSIS
    FillRect ...
    """

    def get_duration_in_ms(self):
        return 3000

    def reset(self):
        self.x = 10

    def update(self, elapsed_ms):
        self.x += elapsed_ms*0.1

    def draw(self, surface):
        surface.fill_rect(self.x, 10, 10, 10, (0.1, 0.5, 0.8))

if __name__ == "__main__":
    run(ExampleAnimation())
