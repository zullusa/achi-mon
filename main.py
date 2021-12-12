import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from classes.command_line_params import CommandLineParams
from classes.decorator import Decorator
from classes.polls import BasePoller, WalletPolling, FarmPolling
from classes.settings import Settings
from classes.telegram import Telebot
from classes.threads import PlotsPollingThread, LogPollingThread, \
    HeartbeatThread


def poll(poller: BasePoller):
    poller.poll()


if __name__ == "__main__":
    clm = CommandLineParams()
    is_test = clm.get("test", False)
    settings = Settings()
    logging.basicConfig(level=logging.getLevelName(settings().get('pollings.log_level', 'WARN')),
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    settings = Settings(settings().get("achi.config.path")) if settings().get("achi.config.path") else settings
    settings().set("runtime.is_test", is_test)
    decorator = Decorator().pre_tags("#hi").embrace_pre()
    telebot = Telebot(settings, decorator)
    telebot.send("\U0001F916 I'm with you. And I started to look after your farming \U0001F499", ding_dong_on=False)
    log_polling_switcher = settings().get("pollings.log.is-on", True)
    farm_polling_switcher = settings().get("pollings.farm.is-on", True)
    plots_polling_switcher = settings().get("pollings.plots.is-on", True)
    wallet_polling_switcher = settings().get("pollings.wallet.is-on", True)
    heartbeat_switcher = settings().get("pollings.heartbeat.is-on", False)
    log_polling = LogPollingThread(settings)
    plots_polling = PlotsPollingThread(settings)
    heartbeat = HeartbeatThread(settings)

    scheduler = BackgroundScheduler()

    if log_polling_switcher:
        log_polling.start()
    if heartbeat_switcher:
        heartbeat.start()

    if wallet_polling_switcher:
        wallet_polling = WalletPolling(settings)
        cron_trigger = CronTrigger.from_crontab(settings().get("pollings.wallet.cron", '* * * * *'), 'Europe/Moscow')
        scheduler.add_job(poll, cron_trigger, args=[wallet_polling])
    if farm_polling_switcher:
        farm_polling = FarmPolling(settings)
        cron_trigger = CronTrigger.from_crontab(settings().get("pollings.farm.cron", '* * * * *'), 'Europe/Moscow')
        scheduler.add_job(poll, cron_trigger, args=[farm_polling])

    if plots_polling_switcher:
        time.sleep(17)
        plots_polling.start()

    scheduler.start()
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
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
