class VideoRenderer:

    """
    >>> process = Process.create_null()
    >>> renderer = VideoRenderer(process=process)
    >>> renderer.render(
    ...     animation=TestAnimation(),
    ...     destination="animation.mp4",
    ...     fps=1,
    ... )
    Render 0
    Write frame1.png
    Render 1000
    Write frame2.png
    Render 2000
    Write frame3.png
    PROCESS =>
      command: ['ffmpeg', '-framerate', '1', '-pattern_type', 'glob', '-i', 'frame*.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'animation.mp4']
    """

    def __init__(self, process):
        self.process = process

    def render(self, animation, destination, fps=25):
        time = 0
        frames = []
        for index in range(animation.get_number_of_frames()):
            time = int(index*1000/fps)
            frame = f"frame{index+1}.png"
            frames.append(frame)
            animation.render(time).write_to_file(frame)
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

    def render(self, time):
        print(f"Render {time}")
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
