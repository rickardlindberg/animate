import cairo
import subprocess

class VideoRenderer:

    """
    >>> process = Process.create_null()
    >>> renderer = VideoRenderer(process=process)
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
      command: ['ffmpeg', '-framerate', '1', '-pattern_type', 'glob', '-i', '/tmp/frame*.png', '-c:v', 'libx264', '-pix_fmt', 'yuva420p', '/tmp/animation.mp4']
    """

    def __init__(self, process):
        self.process = process

    def render(self, animation, destination, fps):
        animation.reset()
        for frame_index in range(int(animation.get_duration_in_ms()/1000*fps)):
            frame = f"/tmp/frame{frame_index+1:04}.png"
            surface = Surface()
            animation.draw(surface)
            surface.write_to_file(frame)
            animation.update(1000/fps)
        self.process.run([
            "ffmpeg",
            "-framerate", f"{fps}",
            "-pattern_type", "glob",
            "-i", "/tmp/frame*.png",
            "-c:v", "libx264",
            "-pix_fmt", "yuva420p",
            destination,
        ])

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

class Surface:

    """
    >>> s = Surface()
    >>> s.fill_rect(0, 0, 10, 10, (0.5, 1, 0.3))
    FillRect =>
      x: 0
    """

    def __init__(self, width=400, height=400):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    def fill_rect(self, x, y, width, height, color):
        print("FillRect =>")
        print(f"  x: {x}")
        ctx = cairo.Context(self.surface)
        ctx.rectangle(x, y, width, height)
        ctx.set_source_rgb(*color)
        ctx.fill()

    def write_to_file(self, destination):
        print(f"Write {destination}")
        self.surface.write_to_png(destination)

class Process:

    @staticmethod
    def create():
        return Process(subprocess)

    @staticmethod
    def create_null():
        class NullSubprocess:
            def run(self, command):
                pass
        return Process(NullSubprocess())

    def __init__(self, subprocess):
        self.subprocess = subprocess

    def run(self, command):
        print("PROCESS =>")
        print(f"  command: {command}")
        self.subprocess.run(command)

if __name__ == "__main__":
    renderer = VideoRenderer(process=Process.create())
    renderer.render(
        animation=TestAnimation(),
        destination="/tmp/animation.mov",
        fps=25,
    )
