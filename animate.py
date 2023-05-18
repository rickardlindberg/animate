import cairo

class VideoRenderer:

    """
    >>> process = Process.create_null()
    >>> renderer = VideoRenderer(process=process)
    >>> renderer.render(
    ...     animation=TestAnimation(),
    ...     destination="animation.mp4",
    ...     fps=1,
    ... )
    Reset
    Render
    Write frame1.png
    Update 1000.0
    Render
    Write frame2.png
    Update 1000.0
    Render
    Write frame3.png
    Update 1000.0
    PROCESS =>
      command: ['ffmpeg', '-framerate', '1', '-pattern_type', 'glob', '-i', 'frame*.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'animation.mp4']
    """

    def __init__(self, process):
        self.process = process

    def render(self, animation, destination, fps):
        animation.reset()
        for index in range(animation.get_number_of_frames()):
            frame = f"frame{index+1}.png"
            surface = Surface()
            animation.draw(surface)
            surface.write_to_file(frame)
            animation.update(1000/fps)
        self.process.run([
            "ffmpeg",
            "-framerate", f"{fps}",
            "-pattern_type", "glob",
            "-i", "frame*.png",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            destination,
        ])

class TestAnimation:

    def get_number_of_frames(self):
        return 3

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
    Render
    """

    def __init__(self, width=400, height=400):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    def fill_rect(self, x, y, width, height, color):
        print("Render")
        ctx = cairo.Context(self.surface)
        ctx.rectangle(x, y, x+width, y+height)
        ctx.set_source_rgb(*color)
        ctx.fill()

    def write_to_file(self, destination):
        print(f"Write {destination}")

class Process:

    @staticmethod
    def create_null():
        return Process()

    def run(self, command):
        print("PROCESS =>")
        print(f"  command: {command}")

if __name__ == "__main__":
    print("Animate")
