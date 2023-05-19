class Preview:

    """
    """

    @staticmethod
    def create():
        return Preview(pygame=pygame)

    @staticmethod
    def create_null():
        return Preview(pygame=NullPygame())

    def __init__(self, pygame):
        self.pygame = pygame

    def run(self, animation):
        pass
