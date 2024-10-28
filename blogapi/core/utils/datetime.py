from datetime import timedelta


def timedelta_isoformat(td: timedelta) -> str:
    """ISO 8601 encoding for Python timedelta object."""
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{"-" if td.days < 0 else
              ""}P{abs(td.days)}DT{hours:0>2}H{minutes:0>2}M{seconds:0>2}S'
