import re

from classes.settings import Settings


class Filter:
    def __init__(self, settings: Settings):
        self.settings = settings.get_settings()

    def apply(self, msg, filter_name):
        patterns = self.settings[filter_name]
        result = ""
        for pattern in patterns:
            match = re.search(pattern, msg, flags=re.MULTILINE)
            if match:
                result += u'\U0001F40C' + ' ' + match[0] + "\n"
        return result
