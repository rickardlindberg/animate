from animationstudio.events import Observable
from animationstudio.graphics import Graphics

class VideoRenderer(Observable):

    """
    >>> isinstance(VideoRenderer.create(), VideoRenderer)
    True
    """

    @staticmethod
    def create():
        return VideoRenderer(
            graphics=Graphics.create(),
        )

    @staticmethod
    def create_null():
        return VideoRenderer(
            graphics=Graphics.create_null(),
        )

    def __init__(self, graphics):
        self.graphics = graphics

    def render(self, animation, destination):
        fps = animation.get_fps()
        animation.reset()
        for frame_index in range(int(animation.get_duration_in_ms()/1000*fps)):
            frame = f"/tmp/frame{frame_index+1:04}.png"
            surface = self.graphics.create_surface(animation.get_size())
            animation.draw(surface)
            surface.write_to_file(frame)
            animation.update(1000/fps)
