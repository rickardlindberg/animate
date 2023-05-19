"""
"""

from animationstudio.animation import Animation
from animationstudio.geometry import Size
from animationstudio.preview import Preview

__all__ = [
    "run",
    "Animation",
    "Size",
    "SIZE_4K",
    "SIZE_HD",
    "SIZE_720",
]

SIZE_4K = Size(width=3840, height=2160)
SIZE_HD = SIZE_4K.scale(0.5)
SIZE_720 = SIZE_HD.scale(0.666667)

def run(animation):
    animation.dry_run()
    Preview.create().run(animation=animation)
