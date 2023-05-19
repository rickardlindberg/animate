from animationstudio.preview import Preview

class Animation:

    def dry_run(self):
        pass

def run(animation):
    Preview.create().run(animation=animation)
