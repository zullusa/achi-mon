import os
import re
import time

from sh import Command

from classes.decorator import Decorator
from classes.settings import Settings
from classes.telegram import Telebot


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


def send_wallet_info(fingerprint, value) -> float:
    decorator = Decorator().pre_emoji(u'\U0001F4B0').embrace_pre().mark_numbers()
    telebot = Telebot(settings, decorator)
    cmd = Command("/opt/achi-blockchain/get_wallet_info.sh")
    output = cmd(fingerprint).stdout.decode(encoding='utf-8')
    match = re.findall(r'-Total Balance:\s?(\d+\.\d+)', output, re.MULTILINE)
    new_val = value
    if match:
        new_val = float(match[0])
        if not value == new_val:
            print(output)
            telebot.send(output)
    return new_val


if __name__ == "__main__":
    settings = Settings()
    fingerprints = settings.get_settings()["wallet.fingerprints"]
    values = {}
    for fingerprint in fingerprints:
        wallet_path = "./wallet_" + str(fingerprint) + ".val"
        values[fingerprint] = read_value_from_file(wallet_path)
    try:
        while True:
            for fingerprint in fingerprints:
                val = send_wallet_info(fingerprint, values[fingerprint])
                wallet_path = "./wallet_" + str(fingerprint) + ".val"
                if not values[fingerprint] == val:
                    values[fingerprint] = val
                    write_value_to_file(wallet_path, val)
            time.sleep(10)
    finally:
        pass
