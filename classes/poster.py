from classes.settings import Settings


class Poster:
    def __init__(self, settings: Settings):
        self.settings = settings()

    def post(self, msg):
        pass
