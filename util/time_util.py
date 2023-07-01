import pytz
from datetime import datetime


def get_current_utc8_time():
    # Get the current time in UTC+8
    utc8_now = datetime.now(pytz.timezone("Asia/Shanghai"))
    return utc8_now
