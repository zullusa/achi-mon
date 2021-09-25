import logging
import time

from classes.decorator import Decorator
from classes.settings import Settings
from classes.telegram import Telebot
from classes.threads import PlotsPollingThread, WalletPollingThread, LogPollingThread, FarmPollingThread, \
    HeartbeatThread

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    settings = Settings()
    settings = Settings(settings().get("achi.config.path")) if settings().get("achi.config.path") else settings
    decorator = Decorator().pre_tags("#hi").embrace_pre()
    telebot = Telebot(settings, decorator)
    telebot.send("\U0001F916 I'm with you. And I started to look after your farming \U0001F499", ding_dong_on=False)
    log_polling_switcher = settings().get("pollings.log.is-on", True)
    farm_polling_switcher = settings().get("pollings.farm.is-on", True)
    plots_polling_switcher = settings().get("pollings.plots.is-on", True)
    wallet_polling_switcher = settings().get("pollings.wallet.is-on", True)
    heartbeat_switcher = settings().get("pollings.heartbeat.is-on", False)
    log_polling = LogPollingThread(settings)
    farm_polling = FarmPollingThread(settings)
    plots_polling = PlotsPollingThread(settings)
    wallet_polling = WalletPollingThread(settings)
    heartbeat = HeartbeatThread(settings)

    if log_polling_switcher:
        log_polling.start()
    if heartbeat_switcher:
        heartbeat.start()
    if farm_polling_switcher:
        time.sleep(13)
        farm_polling.start()
    if plots_polling_switcher:
        time.sleep(17)
        plots_polling.start()
    if wallet_polling_switcher:
        time.sleep(21)
        wallet_polling.start()

    try:
        while True:
            pass
    finally:
        if heartbeat_switcher:
            heartbeat.stop()
            heartbeat.join()
        if log_polling_switcher:
            log_polling.stop()
            log_polling.join()
        if plots_polling_switcher:
            plots_polling.stop()
            plots_polling.join()
        if wallet_polling_switcher:
            wallet_polling.stop()
            wallet_polling.join()
        if farm_polling_switcher:
            farm_polling.stop()
            farm_polling.join()
