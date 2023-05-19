from animationstudio.graphics import Graphics
from animationstudio.process import Process

class TestAnimation:

    def get_duration_in_ms(self):
        return 3000

    def reset(self):
        print("Reset")
        self.x = 10

    def update(self, elapsed_ms):
        print(f"Update {elapsed_ms}")
        self.x += elapsed_ms*0.1

    def draw(self, surface):
        surface.fill_rect(self.x, 10, 10, 10, (0.1, 0.5, 0.8))

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

    def render(self, animation, destination, fps):
        animation.reset()
        for frame_index in range(int(animation.get_duration_in_ms()/1000*fps)):
            frame = f"/tmp/frame{frame_index+1:04}.png"
            surface = self.graphics.create_surface(400, 400)
            animation.draw(surface)
            surface.write_to_file(frame)
            animation.update(1000/fps)
        self.process.run([
            "ffmpeg",
            "-framerate", f"{fps}",
            "-pattern_type", "glob",
            "-i", "/tmp/frame*.png",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            destination,
        ])
