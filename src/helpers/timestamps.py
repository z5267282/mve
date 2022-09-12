import datetime as dt


def get_timestamp():
    right_now = dt.datetime.now()
    return right_now.strftime('%d.%m.%Y - %H%M')

def generate_timestamped_file_name():
    return f'{get_timestamp()}.json'
