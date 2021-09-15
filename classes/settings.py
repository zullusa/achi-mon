from bestconfig import Config


class Settings:
    def __init__(self, path: str = "config.yaml"):
        self.settings = Config(path)

    def __call__(self, *args, **kwargs):
        return self.settings

    def get_settings(self):
        return self.settings
