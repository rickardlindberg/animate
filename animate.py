class Renderer:

    """
    >>> renderer = Renderer()
    >>> renderer.render(animation=TestAnimation(), destination="animation.mp4")
    Render 0
    Write frame1.png
    Render 40
    Write frame2.png
    Render 80
    Write frame3.png
    Compose
      command: ffmpeg -framerate 25 -pattern_type glob -i 'frame*.png' -c:v libx264 -pix_fmt yuv420p animation.mp4
    """

    def render(self, animation, destination, fps=25):
        time = 0
        frames = []
        for index in range(animation.get_number_of_frames()):
            time = int(index*1000/fps)
            animation.render(time)
            frame = f"frame{index+1}.png"
            frames.append(frame)
            print(f"Write {frame}")
        command = [
            "ffmpeg",
            "-framerate", "25",
            "-pattern_type", "glob",
            "-i", "'frame*.png'",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "animation.mp4",
        ]
        print("Compose")
        print(f"  command: {' '.join(command)}")

class TestAnimation:

    def render(self, time):
        print(f"Render {time}")

    def get_number_of_frames(self):
        return 3

if __name__ == "__main__":
    print("Animate")
