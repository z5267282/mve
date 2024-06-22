def get_seconds(time: str) -> int:
    if time.startswith('-'):
        return int(time[1:])

    if ':' in time:
        return get_timestamp_seconds(time)

    return int(time)


def get_timestamp_seconds(timestamp: str) -> int:
    return sum(
        int(t) * (60 ** i)
        for i, t in enumerate(
            reversed(
                timestamp.split(':')
            )
        )
    )
