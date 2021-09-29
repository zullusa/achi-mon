import re

from classes.settings import Settings


class Filter:
    def __init__(self, settings: Settings):
        self.settings = settings.get_settings()

    def apply(self, msg, filter_name, msg_type):
        patterns = self.settings[filter_name]
        result = ""
        for pattern in patterns:
            match = re.findall(pattern, msg, flags=re.MULTILINE)
            if match:
                for m in match:
                    result += "${0}$ {1}\n".format(msg_type, m)
        return result
