from bestconfig import Config


class Settings:
    def __init__(self):
        self.settings = Config("config.yaml")

    def get_settings(self):
        return self.settings
