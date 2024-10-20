import time


def time_convert(timestamp: int) -> str:
    return time.strftime('%d.%m.%Y, %H:%M:%S', time.gmtime(timestamp))