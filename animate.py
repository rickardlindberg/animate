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
    Tick 1000
    Render
    Write frame2.png
    Tick 1000
    Render
    Write frame3.png
    Tick 1000
    PROCESS =>
      command: ['ffmpeg', '-framerate', '1', '-pattern_type', 'glob', '-i', 'frame*.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'animation.mp4']
    """

    def __init__(self, process):
        self.process = process

    def render(self, animation, destination, fps):
        animation.reset()
        time = 0
        frames = []
        for index in range(animation.get_number_of_frames()):
            frame = f"frame{index+1}.png"
            frames.append(frame)
            animation.render().write_to_file(frame)
            animation.update(int(1000/fps))
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

    def reset(self):
        print("Reset")

    def update(self, elapsed_ms):
        print(f"Tick {elapsed_ms}")

    def render(self):
        print("Render")
        return Surface()

    def get_number_of_frames(self):
        return 3

class Surface:

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
