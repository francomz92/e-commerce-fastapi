from datetime import datetime

from ..constants.formats import FORMAT__DATETIME_DMY_A_LAS_HM

class DateFormater:
    @staticmethod
    def to_humanized_date(date: datetime):
        return date.strftime(FORMAT__DATETIME_DMY_A_LAS_HM)