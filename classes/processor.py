import datetime

from classes.filter import Filter
from classes.poster import Poster
from classes.telegram import Telebot


class Processor:

    def __init__(self, poster: Poster, telebot: Telebot, filter: Filter):
        self.poster = poster
        self.telebot = telebot
        self.filter = filter

    def process(self, msg):
        print(datetime.datetime.now(), ">\n", msg)
        telegram_msg = self.filter.apply(msg, "telebot.filters")
        if telegram_msg:
            self.telebot.send(telegram_msg.strip())
        # self.poster.post(msg)
