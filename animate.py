from render import TestAnimation
from render import VideoRenderer

if __name__ == "__main__":
    VideoRenderer.create().render(
        animation=TestAnimation(),
        destination="/tmp/animation.mp4",
        fps=25,
    )
