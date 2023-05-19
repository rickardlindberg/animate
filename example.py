from animationstudio import *

class ExampleAnimation(Animation):

    """
    >>> ExampleAnimation().dry_run() # doctest: +ELLIPSIS
    FillRect =>
      x: 10.0
    FillRect =>
      x: 10
    Write /tmp/frame0001.png
    ...
    FillRect =>
      x: 306.0
    Write /tmp/frame0075.png
    PROCESS =>
      command: ['ffmpeg', '-framerate', '25', '-pattern_type', 'glob', '-i', '/tmp/frame*.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '/tmp/animation.mp4']
    """

    def get_size(self):
        return Size(width=400, height=400)

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
