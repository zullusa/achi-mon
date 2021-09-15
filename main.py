import logging
import time


from classes.decorator import Decorator
from classes.settings import Settings
from classes.telegram import Telebot
from classes.threads import PlotsPollingThread, WalletPollingThread, LogPollingThread, FarmPollingThread

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    settings = Settings()
    settings = Settings(settings().get("achi.config.path")) if settings().get("achi.config.path") else settings
    decorator = Decorator().pre_tags("#hi").embrace_pre()
    telebot = Telebot(settings, decorator)
    telebot.send("\U0001F499 I'm with you. And I started to look after your farming \U0001F482")

    log_polling = LogPollingThread(settings)
    farm_polling = FarmPollingThread(settings)
    plots_polling = PlotsPollingThread(settings)
    wallet_polling = WalletPollingThread(settings)

    log_polling.start()
    time.sleep(13)
    farm_polling.start()
    time.sleep(17)
    plots_polling.start()
    time.sleep(21)
    wallet_polling.start()
    try:
        while True:
            pass
    finally:
        log_polling.stop()
        log_polling.join()
        plots_polling.stop()
        plots_polling.join()
        wallet_polling.stop()
        wallet_polling.join()
        farm_polling.stop()
        farm_polling.join()
