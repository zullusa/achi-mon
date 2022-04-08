import logging
import shutil
import time

from sh import Command

from classes.decorator import Decorator
from classes.settings import Settings
from classes.telegram import Telebot
from classes.wallets import Wallets, Wallet


class BasePoller:
    def poll(self):
        pass


class WalletPolling(BasePoller):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.decorator = Decorator().pre_tags("#wallet").embrace_pre().mark_numbers().set_emoji(
            {"wallet": u'\U0001F4B0'})
        self.telebot = Telebot(self.settings, self.decorator)
        self.logger = logging.root
        self.wallets = Wallets(settings).get_wallets()
        super().__init__()

    def poll(self):
        try:
            for wallet in self.wallets:
                self.__send_wallet_info(wallet())
        except Exception as e:
            self.logger.error(e)

    def __send_wallet_info(self, wallet: Wallet):
        if wallet.value == wallet.prev:
            return
        d = wallet.value - wallet.prev
        delta = "{0:,.4f}".format(abs(d)).replace(',', ' ')
        changing = "\U0001F331 Growing: + {0} ach".format(delta) \
            if d > 0 \
            else "\U0001F342 Fading: - {0} ach".format(delta)
        exp_time = round((time.time() - wallet.prev_time) / 60)
        message = f'$wallet$ {wallet.text}-----------------\n{changing}\n\U0000231B Expected time: {exp_time} min'
        self.logger.info(message)
        self.telebot.send(message, ding_dong_on=self.settings().get("pollings.wallet.ding-dong-on", False), pin=True)


class FarmPolling(BasePoller):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.decorator = Decorator().pre_tags("#farm").embrace_pre().mark_numbers().set_emoji(
            {"summary": u'\U0001F4CA'})
        self.telebot = Telebot(self.settings, self.decorator)
        self.logger = logging.root
        super().__init__()

    def poll(self):
        try:
            self.send_farm_summary()
        except Exception as e:
            self.logger.error(e)
        finally:
            pass

    def send_farm_summary(self):
        cmd = Command(self.settings().get("pollings.farm.command",
                                          self.settings().get("farm.summary.command",
                                                              "/opt/achi-blockchain/get_farm_summary.sh")))
        output = cmd().stdout.decode(encoding='utf-8')
        self.logger.info(output)
        self.telebot.send('$summary$ {0}'.format(output),
                          ding_dong_on=self.settings().get("pollings.farm.ding-dong-on", False))


class DiskspacePolling(BasePoller):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.decorator = Decorator().pre_tags("#diskusage").embrace_pre().mark_numbers().set_emoji(
            {"disk": u'\U0001F4BE'})
        self.telebot = Telebot(self.settings, self.decorator)
        self.logger = logging.root
        super().__init__()

    def poll(self):
        try:
            self.check_disks()
        except Exception as e:
            self.logger.error(e)
        finally:
            pass

    def check_disks(self):
        gb = 1024 * 1024 * 1024
        disks = self.settings().get("pollings.diskspace.disks", ('/', '/home'))
        threshold = self.settings().get("pollings.diskspace.alert-threshold", 10)
        for disk in disks:
            t, u, f = shutil.disk_usage(disk)
            if ((f / t) * 100.0) <= threshold:
                text = "Disk mounted on '{0}'" \
                       "\n\thas insufficient space (less {4}%):" \
                       "\n\t\tTotal:\t{1:.2f} GiB," \
                       "\n\t\tUsage:\t{2:.2f} GiB," \
                       "\n\t\tFree:\t{3:.2f} GiB".format(disk, t/gb, u/gb, f/gb, threshold)
                self.logger.info(text)
                self.telebot.send('$disk$ {0}'.format(text),
                                  ding_dong_on=self.settings().get("pollings.diskspace.ding-dong-on", False))


