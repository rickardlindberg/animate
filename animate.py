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
    Compose frame1.png frame2.png frame3.png
    """

    def render(self, animation, destination):
        time = 0
        frames = []
        for index in range(animation.get_number_of_frames()):
            animation.render(time)
            time += 40
            frame = f"frame{index+1}.png"
            frames.append(frame)
            print(f"Write {frame}")
        print(f"Compose {' '.join(frames)}")

class TestAnimation:

    def render(self, time):
        print(f"Render {time}")

    def get_number_of_frames(self):
        return 3

if __name__ == "__main__":
    print("Animate")
