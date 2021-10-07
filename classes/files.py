import json
import logging
import os


def read_json_from_file(file_path):
    value = None
    if os.path.isfile(file_path):
        with open(file_path, 'r') as _file:
            value = json.load(_file)
    return value


def write_json_to_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as _file:
        json.dump(data, _file, ensure_ascii=False, indent=4)


def write_value_to_file(file_path, value):
    _file = open(file_path, 'w')
    try:
        _file.write(str(value))
        _file.flush()
    except Exception as e:
        logging.root.error(f'Error: {e}')
    finally:
        _file.close()


def read_value_from_file(file_path) -> float:
    value = 0.0
    if os.path.isfile(file_path):
        _file = open(file_path, 'r')
        try:
            _file.seek(0)
            value = float(_file.read(-1).strip())
        except Exception as err:
            logging.root.error("Error: {0}".format(err))
        finally:
            _file.close()
    return value
