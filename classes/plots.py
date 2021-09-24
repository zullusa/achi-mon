import json
import logging
import os


def count_plots(path: str):
    count = 0
    size = 0
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name.endswith(".plot"):
            count += 1
            size += os.path.getsize(os.path.join(path, name))
    return count, size


class Counter:

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.values = self.__read_values_from_file(file_name)
        self.logger = logging.root

    def save(self):
        _file = open(self.file_name, 'w')
        try:
            _file.write(str(json.JSONEncoder().encode(self.values)))
        except Exception as e:
            self.logger.error("Error: {0}".format(e))
        finally:
            _file.close()

    def is_different_total(self, new_total) -> bool:
        total = 0 if not 'total' in self.values.keys() else self.values['total']
        if new_total != total:
            self.values['total'] = new_total
            return True
        else:
            return False

    def is_different(self, path: str, new_count: int) -> bool:
        count = self.__get_count_for_path(path)
        if new_count != count:
            self.values['paths'][path] = new_count
            return True
        return False

    def __get_count_for_path(self, path) -> int:
        count = 0
        if path in self.values['paths'].keys():
            return self.values['paths'][path]
        else:
            self.values['paths'][path] = count
        return count

    def __read_values_from_file(self, file_name: str) -> dict:
        values = {'total': 0, 'paths': {}}
        if os.path.isfile(file_name):
            _file = open(file_name, 'r')
            try:
                _file.seek(0)
                values = json.load(_file.read(-1))
            except Exception as err:
                self.logger.error("Error: {0}".format(err))
            finally:
                _file.close()
        return values
