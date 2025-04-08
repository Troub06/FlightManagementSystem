from datetime import datetime
from src.configs import *

class DatetimeChecker:
    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, DATE_FORMAT)
            return True
        except ValueError:
            return False

    def is_valid_time(self, time_str):
        try:
            datetime.strptime(time_str, TIME_FORMAT)
            return True
        except ValueError:
            return False
