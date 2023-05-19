from animationstudio.animation import Animation
from animationstudio.preview import Preview

__all__ = ["run", "Animation"]

def run(animation):
    animation.dry_run()
    Preview.create().run(animation=animation)
