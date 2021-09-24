import logging
import os
import re
import threading
import time

import requests
from sh import Command
from watchdog.observers import Observer

from classes import plots
from classes.decorator import Decorator
from classes.filter import Filter
from classes.plots import Counter
from classes.poster import Poster
from classes.processor import Processor
from classes.settings import Settings
from classes.telegram import Telebot


def write_value_to_file(file_path, value):
    _file = open(file_path, 'w')
    try:
        _file.write(str(value))
    except Exception as e:
        logging.root.error("Error: {0}".format(e))
    finally:
        _file.close()


def read_value_from_file(file_path) -> float:
    value = 0.0
    if os.path.isfile(file_path):
        _file = open(file_path, 'r')
        try:
            _file.seek(0)
            value = float(_file.read(-1).strip())
        except Exception as err:
            logging.root.error("Error: {0}".format(err))
        finally:
            _file.close()
    return value


class PlotsPollingThread(threading.Thread):

    def __init__(self, settings: Settings):
        self.settings = settings
        self.decorator = Decorator().pre_tags("#plots"). \
            embrace_pre().mark_numbers(). \
            set_emoji({"plot": u'\U0001F4E6', "plus": u'\U00002795'})
        self.telebot = Telebot(self.settings, self.decorator)
        self.logger = logging.root
        super().__init__()

    def run(self) -> None:
        counter = Counter('plot_count.ext.val')
        paths = self.settings().get("harvester.plot_directories") or self.settings().get("plots.paths")
        interval = float(self.settings().get("pollings.plots.interval", 60))
        info = "$plot$ Total count: {0} plot(s)\nTotal plots size: {2:.3f} TiB\nSummary:\n{1}"
        try:
            while True:
                total_count = 0
                total_size = 0
                path_txt = " {3}{0} - {1} plot(s) ( {2:.3f} GiB )\n"
                total_txt = ""
                for plots_path in paths:
                    count, size = plots.count_plots(plots_path)
                    if counter.is_different(plots_path, count):
                        bullet = '$plus$'
                    else:
                        bullet = '- '
                    total_count += count
                    total_size += size
                    total_txt += path_txt.format(plots_path, count, size / (1024 ** 3), bullet)
                if counter.is_different_total(total_count):
                    self.__send_msg(info.format(total_count, total_txt, total_size / (1024 ** 4)))
                    counter.save()
                time.sleep(60 * interval)
        finally:
            pass

    def __send_msg(self, msg):
        self.telebot.send(msg, ding_dong_on=self.settings().get("pollings.plots.ding-dong-on", False))

    def stop(self):
        pass


class WalletPollingThread(threading.Thread):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.decorator = Decorator().pre_tags("#wallet").embrace_pre().mark_numbers().set_emoji(
            {"wallet": u'\U0001F4B0'})
        self.telebot = Telebot(self.settings, self.decorator)
        self.logger = logging.root
        super().__init__()

    def run(self) -> None:
        fingerprints = self.settings().get("my_wallet.fingerprints")
        interval = self.settings().get("my_wallet.interval")
        values = {}
        for fingerprint in fingerprints:
            wallet_path = "./wallet_" + str(fingerprint) + ".val"
            values[fingerprint] = read_value_from_file(wallet_path)
        try:
            while True:
                for fingerprint in fingerprints:
                    wallet_path = "./wallet_" + str(fingerprint) + ".val"
                    val = self.send_wallet_info(fingerprint, values[fingerprint], os.path.getmtime(wallet_path))
                    if values[fingerprint] != val:
                        values[fingerprint] = val
                        write_value_to_file(wallet_path, val)
                time.sleep(60 * interval)
        finally:
            pass

    def send_wallet_info(self, fingerprint, value, prev_time: float = time.time()) -> float:
        cmd = Command(self.settings().get("my_wallet.command"))
        output = cmd(fingerprint).stdout.decode(encoding='utf-8')
        match = re.findall(r'-Total Balance:\s?(\d+\.\d+)', output, re.MULTILINE)
        new_val = value
        if match:
            new_val = float(match[0])
            if value != new_val:
                self.logger.info(output)
                growing = "\U0001F331 Growing: + {0:.4f} xach".format((new_val - value)) \
                    if new_val > value \
                    else "\U0001F342 Fading: - {0:.4f} xach".format((value - new_val))
                exp_time = (time.time() - prev_time) / 60
                self.telebot.send("$wallet$ {0}-----------------\n{1}\n\U0000231B Expected time: {2:.2f} min"
                                  .format(output, growing, exp_time),
                                  ding_dong_on=self.settings().get("pollings.wallet.ding-dong-on", False))
        return new_val

    def stop(self):
        pass


class LogPollingThread(threading.Thread):

    def __init__(self, settings: Settings):
        self.settings = settings
        super().__init__()

    def run(self):
        path = self.settings().get("logs.logfile")
        poster = Poster(self.settings)
        decorator = Decorator() \
            .embrace_pre() \
            .pre_tags("#log") \
            .mark_numbers() \
            .set_emoji({'msg': u'\U0001F40C', 'error': u'\U0000203C'})
        telebot = Telebot(self.settings, decorator)
        msg_filter = Filter(self.settings)
        processor = Processor(poster, telebot, msg_filter, self.settings)
        from classes.handler import LogModifiedHandler
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

    def stop(self):
        pass


class FarmPollingThread(threading.Thread):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.decorator = Decorator().pre_tags("#farm").embrace_pre().mark_numbers().set_emoji(
            {"summary": u'\U0001F4CA'})
        self.telebot = Telebot(self.settings, self.decorator)
        self.logger = logging.root
        super().__init__()

    def run(self) -> None:
        interval = self.settings().get("farm.summary.interval")
        try:
            while True:
                self.send_farm_summary()
                time.sleep(60 * interval)
        finally:
            pass

    def send_farm_summary(self):
        cmd = Command(self.settings().get("farm.summary.command"))
        output = cmd().stdout.decode(encoding='utf-8')
        self.logger.info(output)
        self.telebot.send('$summary$ {0}'.format(output),
                          ding_dong_on=self.settings().get("pollings.farm.ding-dong-on", False))

    def stop(self):
        pass


class HeartbeatThread(threading.Thread):

    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = logging.root
        super().__init__()

    def run(self) -> None:
        interval = self.settings().get("pollings.heartbeat.interval", 1)
        api = self.settings().get("pollings.heartbeat.api", "https://api.gimro.ru/dummybeat")
        token = self.settings().get("pollings.heartbeat.token", "test")
        try:
            while True:
                self.__beat(api, token)
                time.sleep(60 * interval)
        finally:
            pass

    def stop(self):
        pass

    def __beat(self, api: str, token: str):
        url = "{0}?token={1}".format(api, token)
        try:
            r = requests.get(url=url)
            if r.status_code != 200:
                self.logger.error(r.text)
            else:
                self.logger.info(r.text)
        except Exception as e:
            self.logger.error(e)
