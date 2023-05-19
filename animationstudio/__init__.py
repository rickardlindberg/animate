from animationstudio.animation import Animation
from animationstudio.geometry import Size
from animationstudio.preview import Preview

__all__ = [
    "run",
    "Animation",
    "Size",
]

def run(animation):
    animation.dry_run()
    Preview.create().run(animation=animation)
