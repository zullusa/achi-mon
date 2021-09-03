import os
import time

from classes.decorator import Decorator
from classes.settings import Settings
from classes.telegram import Telebot


def send_msg(msg):
    decorator = Decorator().pre_emoji(u'\U0001F4E6').embrace_pre().mark_numbers()
    telebot = Telebot(settings, decorator)
    telebot.send(msg)


def count_plots(path):
    count = 0
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name.endswith(".plot"):
            count += 1
    return count


if __name__ == "__main__":
    settings = Settings()
    paths = settings.get_settings()["plots.paths"]
    interval = float(settings.get_settings()["plots.interval"] if settings.get_settings()["plots.interval"] else 60)
    info = "Total file count {0} :\n{1}"
    if len(paths) == 0:
        exit(234)

    try:
        while True:
            total_sum = 0
            txt = "  - {0} - {1} plot(s)\n"
            total = ""
            for plots_path in paths:
                val = count_plots(plots_path)
                total_sum += val
                total += txt.format(plots_path, val)
            send_msg(info.format(total_sum, total))
            time.sleep(60 * interval)
    finally:
        pass
