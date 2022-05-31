import datetime as dt
import json
import sys

def write_to_json(item, file_path):
    with open(file_path, 'w') as f:
        json.dump(item, f, indent=4)

def read_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def get_timestamp():
    right_now = dt.datetime.now()
    return right_now.strftime('%d.%m.%Y - %H%M')

def stderr_print(message):
    print(message, file=sys.stderr)
