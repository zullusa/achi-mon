import logging
import os
import sys

from watchdog.observers import Observer

from classes.decorator import Decorator
from classes.filter import Filter
from classes.handler import LogModifiedHandler
from classes.poster import Poster
from classes.processor import Processor
from classes.settings import Settings
from classes.telegram import Telebot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else './test/test.log'
    settings = Settings()
    poster = Poster(settings)
    decorator = Decorator().embrace_pre().pre_emoji(u'\U0001F40C')
    telebot = Telebot(settings, decorator)
    filter = Filter(settings)
    processor = Processor(poster, telebot, filter)
    event_handler = LogModifiedHandler(path, processor)
    observer = Observer()
    observer.schedule(event_handler, os.path.split(path)[0])
    observer.start()
    try:
        while True:
            pass
    finally:
        observer.stop()
        observer.join()
