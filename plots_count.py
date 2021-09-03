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
    size = 0
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name.endswith(".plot"):
            count += 1
            size += os.path.getsize(os.path.join(path, name))
    return count, size


if __name__ == "__main__":
    settings = Settings()
    paths = settings.get_settings()["plots.paths"]
    interval = float(settings.get_settings()["plots.interval"] if settings.get_settings()["plots.interval"] else 60)
    info = "Total plots count : {0}\nTotal plots size: {2:.3f} TiB\nSummary:\n{1}"
    if len(paths) == 0:
        exit(234)

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
            send_msg(info.format(total_count, total, total_size / (1024 ** 4)))
            time.sleep(60 * interval)
    finally:
        pass
