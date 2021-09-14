import time

import requests

from classes.decorator import Decorator
from classes.settings import Settings


class Telebot:

    def __init__(self, settings: Settings, decorator: Decorator):
        self.settings = settings.get_settings()
        self.decorator = decorator

    def send(self, text: str, is_error: bool = False, trying: int = 0):
        token = self.settings["telebot.api-key"]
        url = "https://api.telegram.org/bot"
        channel_id = self.settings["telebot.channel"]
        url += token
        method = url + "/sendMessage"
        if is_error:
            msg = self.decorator.format_text(text, supply_tags='#error')
        else:
            msg = self.decorator.format_text(text)
        try:
            r = requests.post(method, data={
                "chat_id": channel_id,
                "text": msg,
                "parse_mode": "HTML",
                "disable_notification": True
            })
        except Exception as e:
            print(e)
            if trying <= 0:
                time.sleep(5)
                print('Trying #2')
                self.send(str, is_error, trying + 1)

        if r.status_code != 200:
            print(r.text)
            print(msg)
