import logging
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
        delta = wallet.value - wallet.prev
        growing = "\U0001F331 Growing: + {0:.4f} xach".format(delta) \
            if delta > 0 \
            else "\U0001F342 Fading: - {0:.4f} xach".format(abs(delta))
        exp_time = round((time.time() - wallet.prev_time) / 60)
        message = f'$wallet$ {wallet.text}-----------------\n{growing}\n\U0000231B Expected time: {exp_time} min'
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

