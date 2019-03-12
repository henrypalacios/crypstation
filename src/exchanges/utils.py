import datetime
import pytz


def parse_datetime(timestamp: int, has_milliseconds=True):
    """
    Convert date from timestamp to date in format '2018-01-01 01:00:00'
    in utc (not local timezone)

    :param timestamp:
    :return:
    """
    if has_milliseconds:
        timestamp = timestamp / 1000

    time = datetime.datetime\
        .fromtimestamp(timestamp, tz=pytz.utc) \

    return time