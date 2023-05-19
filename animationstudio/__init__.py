from animationstudio.preview import Preview
from animationstudio.render import VideoRenderer

__all__ = ["run", "Animation"]

class Animation:

    def dry_run(self):
        Preview.create_null().run(animation=self)
        VideoRenderer.create_null().render(animation=self, fps=25, destination="/tmp/animation.mp4")

def run(animation):
    Preview.create().run(animation=animation)
