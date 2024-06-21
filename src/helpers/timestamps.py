import datetime as dt


def get_timestamp() -> str:
    right_now = dt.datetime.now()
    return right_now.strftime('%d.%m.%Y - %H%M')


def generate_timestamped_file_name() -> str:
    return f'{get_timestamp()}.json'
