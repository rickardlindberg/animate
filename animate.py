from animations.test import TestAnimation
from preview import Preview

if __name__ == "__main__":
    Preview.create().render(
        animation=TestAnimation(),
        destination="/tmp/animation.mp4",
        fps=25,
    )
