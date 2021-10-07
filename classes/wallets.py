import os
import re
import time

from sh import Command

from classes.files import read_json_from_file, write_json_to_file
from classes.settings import Settings


class Wallets:

    def __init__(self, settings: Settings):
        self.settings = settings()
        self.cmd = Command(self.settings.get('pollings.wallet.command', self.settings.get("my_wallet.command")))

    def get_wallets(self):
        fingerprints = self.settings.get('pollings.wallet.fingerprints', self.settings.get("my_wallet.fingerprints"))
        wallets = []
        for fingerprint in fingerprints:
            wallets.append(Wallet(fingerprint, self.cmd))
        return wallets


class Wallet:

    def __init__(self, fingerprint, cmd):
        self.fingerprint = fingerprint
        self.cmd = cmd
        self.value = 0.0
        self.prev = 0.0
        self.text = ''
        self.prev_time = time.time()

    def __call__(self):
        self.text = self.cmd(self.fingerprint).stdout.decode(encoding='utf-8')
        match = re.findall(r'-Total Balance:\s?(\d+\.\d+)', self.text, re.MULTILINE)
        if match:
            self.value = float(match[0])
        self.prev, self.prev_time = self.__read_previous_value_from_file()
        if self.prev != self.value:
            self.__write_previous_value_from_file()
        return self

    def to_dict(self) -> dict:
        return {"fingerprint": self.fingerprint,
                "value": self.value,
                "prev": self.prev,
                "prev_time": self.prev_time,
                "text": self.text}

    def __read_previous_value_from_file(self):
        value = 0.0
        file_path = "./wallet_" + str(self.fingerprint) + ".val"
        wallet = read_json_from_file(file_path)
        if wallet:
            value = wallet.get('value')
        return value, os.path.getmtime(file_path)

    def __write_previous_value_from_file(self):
        data = {'value': self.value}
        file_path = "./wallet_" + str(self.fingerprint) + ".val"
        write_json_to_file(file_path, data)
