import logging

from classes.filter import Filter
from classes.poster import Poster
from classes.telegram import Telebot


class Processor:

    def __init__(self, poster: Poster, telebot: Telebot, filter: Filter):
        self.poster = poster
        self.telebot = telebot
        self.filter = filter
        self.logger = logging.root

    def process(self, msg):
        self.logger.info("\n{0}".format(msg))
        telegram_msg = self.filter.apply(msg, "logs.filters.messages", "msg")
        telegram_err = self.filter.apply(msg, "logs.filters.errors", "error")
        if telegram_msg:
            self.telebot.send(telegram_msg.strip())
        if telegram_err:
            self.telebot.send(telegram_err.strip(), is_error=True)
