from animationstudio.geometry import Size

class Animation:

    def dry_run(self):
        from animationstudio.preview import Preview
        from animationstudio.render import VideoRenderer
        Preview.create_null().run(animation=self)
        VideoRenderer.create_null().render(animation=self, destination="/tmp/animation.mp4")

    def get_size(self):
        return Size(width=400, height=400)

    def get_fps(self):
        return 25

    def get_duration_in_ms(self):
        return 1000

    def reset(self):
        pass

    def update(self, elapsed_ms):
        pass

    def draw(self, surface):
        pass
