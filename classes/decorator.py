import re


class Decorator:

    def __init__(self):
        self.text = ''
        self.formatted_text = ''
        self.tags = ''
        self.need_mark_numbers = False
        self.need_pre = False
        self.emojis = {}

    def set_emoji(self, emojis: dict):
        self.emojis = emojis
        return self

    def mark_numbers(self):
        self.need_mark_numbers = True
        return self

    def pre_tags(self, tags: str):
        self.tags = tags
        return self

    def embrace_pre(self):
        self.need_pre = True
        return self

    def format_text(self, text, supply_tags: str = ''):
        self.__set_text(text)
        if self.need_pre and not self.need_mark_numbers:
            self.formatted_text = '`' + self.formatted_text + '`'
        elif self.need_pre and self.need_mark_numbers:
            self.__make_numbers_with_pre()
        elif not self.need_pre and self.need_mark_numbers:
            self.__make_numbers()
        else:
            pass
        if self.tags:
            self.formatted_text = "{0} {1}\n".format(self.tags, supply_tags) + self.formatted_text
        for emoji in self.emojis.keys():
            self.formatted_text = self.formatted_text.replace("${0}$".format(emoji), self.emojis.get(emoji))
        return self.formatted_text

    def __make_numbers_with_pre(self):
        txt = self.text
        match = re.findall(r'(\s\d+\.?\d+\s|\s\d+\s)', txt, flags=re.MULTILINE)
        already = []
        if match:
            for m in match:
                if m not in already:
                    txt = txt.replace(m, " `*{0}*` ".format(m))
                    already.append(m)
        self.formatted_text = '`' + txt + '`'

    def __make_numbers(self):
        txt = self.text
        match = re.findall(r'(\s\d+\.?\d+\s|\s\d+\s)', txt, flags=re.MULTILINE)
        already = []
        if match:
            for m in match:
                if m not in already:
                    txt = txt.replace(m, "*{0}*".format(m))
                    already.append(m)
        self.formatted_text = txt

    def __set_text(self, text):
        self.text = text
        self.formatted_text = text
        return self
