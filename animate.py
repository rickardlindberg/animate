from animations.test import TestAnimation
from preview import Preview

if __name__ == "__main__":
    Preview.create().run(
        animation=TestAnimation(),
    )
