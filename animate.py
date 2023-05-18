class Renderer:

    """
    >>> renderer = Renderer()
    >>> renderer.render(animation=TestAnimation(), destination="animation.mp4")
    Write frame1.png
    Write frame2.png
    Write frame3.png
    Compose frame1.png frame2.png frame3.png
    """

    def render(self, animation, destination):
        frames = []
        for index in range(animation.get_number_of_frames()):
            frame = f"frame{index+1}.png"
            frames.append(frame)
            print(f"Write {frame}")
        print(f"Compose {' '.join(frames)}")

class TestAnimation:

    def get_number_of_frames(self):
        return 3

if __name__ == "__main__":
    print("Animate")
