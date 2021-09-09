import os
import re
import threading
import time

from sh import Command

from classes.decorator import Decorator
from classes.settings import Settings
from classes.telegram import Telebot


def count_plots(path):
    count = 0
    size = 0
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name.endswith(".plot"):
            count += 1
            size += os.path.getsize(os.path.join(path, name))
    return count, size


def write_value_to_file(file_path, value):
    wallet_file = open(file_path, 'w')
    try:
        wallet_file.write(str(value))
    except Exception as e:
        print("Error: {0}".format(e))
    finally:
        wallet_file.close()


def read_value_from_file(wallet_path) -> float:
    value = 0.0
    if os.path.isfile(wallet_path):
        file = open(wallet_path, 'r')
        try:
            file.seek(0)
            value = float(file.read(-1).strip())
        except Exception as err:
            print("Error: {0}".format(err))
        finally:
            file.close()
    return value


class PlotsPollingThread(threading.Thread):

    def __init__(self, settings: Settings):
        self.settings = settings
        self.decorator = Decorator().pre_tags("#plots").embrace_pre().mark_numbers().set_emoji({"plot": u'\U0001F4E6'})
        self.telebot = Telebot(self.settings, self.decorator)
        super().__init__()

    def run(self) -> None:
        paths = self.settings.get_settings()["plots.paths"]
        interval = float(self.settings.get_settings()["plots.interval"]
                         if self.settings.get_settings()["plots.interval"] else 60)
        info = "$plot$ Total count: {0} plot(s)\nTotal plots size: {2:.3f} TiB\nSummary:\n{1}"
        try:
            while True:
                total_count = 0
                total_size = 0
                txt = " - {0} - {1} plot(s) ( {2:.3f} GiB )\n"
                total = ""
                for plots_path in paths:
                    val, size = count_plots(plots_path)
                    total_count += val
                    total_size += size
                    total += txt.format(plots_path, val, size / (1024 ** 3))
                self.__send_msg(info.format(total_count, total, total_size / (1024 ** 4)))
                time.sleep(60 * interval)
        finally:
            pass

    def __send_msg(self, msg):
        self.telebot.send(msg)

    def stop(self):
        pass


class WalletPollingThread(threading.Thread):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.decorator = Decorator().pre_tags("#wallet").embrace_pre().mark_numbers().set_emoji({"wallet": u'\U0001F4B0'})
        self.telebot = Telebot(self.settings, self.decorator)
        super().__init__()

    def run(self) -> None:
        fingerprints = self.settings.get_settings()["wallet.fingerprints"]
        interval = self.settings.get_settings()["wallet.interval"]
        values = {}
        for fingerprint in fingerprints:
            wallet_path = "./wallet_" + str(fingerprint) + ".val"
            values[fingerprint] = read_value_from_file(wallet_path)
        try:
            while True:
                for fingerprint in fingerprints:
                    val = self.send_wallet_info(fingerprint, values[fingerprint])
                    wallet_path = "./wallet_" + str(fingerprint) + ".val"
                    if not values[fingerprint] == val:
                        values[fingerprint] = val
                        write_value_to_file(wallet_path, val)
                time.sleep(60 * interval)
        finally:
            pass

    def send_wallet_info(self, fingerprint, value) -> float:
        cmd = Command(self.settings.get_settings()["wallet.command"])
        output = cmd(fingerprint).stdout.decode(encoding='utf-8')
        match = re.findall(r'-Total Balance:\s?(\d+\.\d+)', output, re.MULTILINE)
        new_val = value
        if match:
            new_val = float(match[0])
            if not value == new_val:
                print(output)
                self.telebot.send('$wallet$ {0}'.format(output))
        return new_val
