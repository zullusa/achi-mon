import argparse
import sys


class CommandLineParams:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--test', nargs='?')
        args = parser.parse_args(sys.argv[1:])
        self.params = args.__dict__

    def get(self, name, default_value):
        val = self.params.get(name)
        if val:
            return val
        else:
            return default_value
