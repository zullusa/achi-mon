import logging
import os
import time

from watchdog.observers import Observer

from classes.decorator import Decorator
from classes.filter import Filter
from classes.handler import LogModifiedHandler
from classes.poster import Poster
from classes.processor import Processor
from classes.settings import Settings
from classes.telegram import Telebot
from classes.threads import PlotsPollingThread, WalletPollingThread

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    settings = Settings()
    path = settings.get_settings()["logs.logfile"]
    poster = Poster(settings)
    decorator = Decorator() \
        .embrace_pre() \
        .pre_tags("#log") \
        .mark_numbers() \
        .set_emoji({'msg': u'\U0001F40C', 'error': u'\U0000203C'})
    telebot = Telebot(settings, decorator)
    telebot.send("\n\U00002764 I'm with you. And I started to look after your farming")
    msg_filter = Filter(settings)
    processor = Processor(poster, telebot, msg_filter)
    event_handler = LogModifiedHandler(path, processor)
    observer = Observer()
    observer.schedule(event_handler, os.path.split(path)[0])
    observer.start()
    plots_polling = PlotsPollingThread(settings)
    wallet_polling = WalletPollingThread(settings)
    time.sleep(20)
    wallet_polling.start()
    time.sleep(20)
    plots_polling.start()
    try:
        while True:
            pass
    finally:
        observer.stop()
        observer.join()
        plots_polling.stop()
        plots_polling.join()
        wallet_polling.stop()
        wallet_polling.join()
