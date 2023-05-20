from animationstudio.graphics import Graphics
from animationstudio.process import Process

class VideoRenderer:

    """
    >>> isinstance(VideoRenderer.create(), VideoRenderer)
    True
    """

    @staticmethod
    def create():
        return VideoRenderer(
            process=Process.create(),
            graphics=Graphics.create(),
        )

    @staticmethod
    def create_null():
        return VideoRenderer(
            process=Process.create_null(),
            graphics=Graphics.create_null(),
        )

    def __init__(self, process, graphics):
        self.process = process
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
