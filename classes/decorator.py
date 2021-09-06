import re

from classes.settings import Settings


class Decorator:

    def __init__(self):
        self.text = ''
        self.formatted_text = ''
        self.tags = ''
        self.need_mark_numbers = False
        self.need_pre = False

    def __set_text(self, text):
        self.text = text
        self.formatted_text = text
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

    def format_text(self, text):
        self.__set_text(text)
        if self.need_pre and not self.need_mark_numbers:
            self.formatted_text = '<pre>' + self.formatted_text + '</pre>'
        elif self.need_pre and self.need_mark_numbers:
            self.__make_numbers_with_pre()
        elif not self.need_pre and self.need_mark_numbers:
            self.__make_numbers()
        else:
            pass
        if self.tags:
            self.formatted_text = self.tags + "\n" + self.formatted_text
        return self.formatted_text

    def __make_numbers_with_pre(self):
        txt = self.text
        match = re.findall(r'(\s\d+\.?\d+\s|\s\d+\s)', txt, flags=re.MULTILINE)
        already = []
        if match:
            for m in match:
                if m not in already:
                    txt = txt.replace(m, "</pre><strong>{0}</strong><pre>".format(m))
                    already.append(m)
        self.formatted_text = '<pre>' + txt + '</pre>'

    def __make_numbers(self):
        txt = self.text
        match = re.findall(r'(\s\d+\.?\d+\s|\s\d+\s)', txt, flags=re.MULTILINE)
        already = []
        if match:
            for m in match:
                if m not in already:
                    txt = txt.replace(m, " <strong>{0}</strong> ".format(m))
                    already.append(m)
        self.formatted_text = txt
