from animationstudio.examples import TestAnimation
from animationstudio.graphics import Graphics
from animationstudio.process import Process

class VideoRenderer:

    """
    >>> process = Process.create_null()
    >>> graphics = Graphics.create_null()
    >>> renderer = VideoRenderer(process=process, graphics=graphics)
    >>> renderer.render(
    ...     animation=TestAnimation(),
    ...     destination="/tmp/animation.mp4",
    ...     fps=1,
    ... )
    Reset
    FillRect =>
      x: 10
    Write /tmp/frame0001.png
    Update 1000.0
    FillRect =>
      x: 110.0
    Write /tmp/frame0002.png
    Update 1000.0
    FillRect =>
      x: 210.0
    Write /tmp/frame0003.png
    Update 1000.0
    PROCESS =>
      command: ['ffmpeg', '-framerate', '1', '-pattern_type', 'glob', '-i', '/tmp/frame*.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '/tmp/animation.mp4']
    """

    @staticmethod
    def create():
        return VideoRenderer(
            process=Process.create(),
            graphics=Graphics.create(),
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
