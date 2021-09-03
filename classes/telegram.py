import requests

from classes.decorator import Decorator
from classes.settings import Settings


class Telebot:

    def __init__(self, settings: Settings, decorator: Decorator):
        self.settings = settings.get_settings()
        self.decorator = decorator

    def send(self, text: str):
        token = self.settings["telebot.api-key"]
        url = "https://api.telegram.org/bot"
        channel_id = self.settings["telebot.channel"]
        url += token
        method = url + "/sendMessage"
        msg = self.decorator.format_text(text)

        r = requests.post(method, data={
            "chat_id": channel_id,
            "text": msg,
            "parse_mode": "HTML",
            "disable_notification": True
        })

        if r.status_code != 200:
            print(r.text)
            print(msg)

# if __name__ == '__main__':
#     send_telegram("hello world!")
