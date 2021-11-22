import logging
import time

import requests

from classes.decorator import Decorator
from classes.settings import Settings


class Telebot:

    def __init__(self, settings: Settings, decorator: Decorator):
        self.settings = settings.get_settings()
        self.decorator = decorator
        self.logger = logging.root
        self.trying_count = self.settings.get("telebot.send_trying_count", 1)

    def send(self, text: str, is_error: bool = False, trying: int = 0, ding_dong_on: bool = True, pin: bool = False):
        if self.settings.get("runtime.is_test"):
            return
        token = self.settings.get("telebot.api-key")
        bot_id = self.settings.get("telebot.bot_id")
        url = "https://api.telegram.org/bot"
        channel_id = self.settings["telebot.channel"]
        url += token
        if is_error:
            msg = self.decorator.format_text(text, supply_tags='#error')
        else:
            msg = self.decorator.format_text(text)
        try:
            r = requests.post(url + '/sendMessage', data={
                "chat_id": channel_id,
                "text": ("#{0} ".format(bot_id) if bot_id else "") + msg,
                "parse_mode": "HTML",
                "disable_notification": not ding_dong_on
            })

            if r.status_code != 200:
                self.logger.error(r.text)
                self.logger.info(msg)
            else:
                if pin:
                    message_id = r.json()['result']['message_id']
                    print('Message ID', message_id)
                    r = requests.post(url + '/pinChatMessage', data={
                        "chat_id": channel_id,
                        "message_id": message_id,
                        "disable_notification": not ding_dong_on
                    })
        except Exception as e:
            self.logger.error(e)
            if trying < self.trying_count:
                time.sleep(5)
                self.logger.info('Trying #{0} ...'.format(trying + 1))
                self.send(str, is_error, trying + 1)


