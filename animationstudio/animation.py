class Animation:

    def dry_run(self):
        from animationstudio.preview import Preview
        from animationstudio.render import VideoRenderer
        Preview.create_null().run(animation=self)
        VideoRenderer.create_null().render(animation=self, fps=25, destination="/tmp/animation.mp4")

    def get_duration_in_ms(self):
        return 1000

    def reset(self):
        pass

    def update(self, elapsed_ms):
        pass

    def draw(self, surface):
        pass
