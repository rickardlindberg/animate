from animationstudio.animation import Animation
from animationstudio.preview import Preview

__all__ = ["run", "Animation"]

def run(animation):
    Preview.create().run(animation=animation)
