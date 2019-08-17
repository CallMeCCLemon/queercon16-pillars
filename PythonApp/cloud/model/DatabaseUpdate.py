###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from datetime import datetime

from PythonApp.cloud.model import BadgeType
from PythonApp.qc_serial.model import CurrencyType


class DatabaseUpdate:
    def __init__(self,
                 badge_id: int,
                 badge_type: BadgeType,
                 creation_time: datetime,
                 currency_type: CurrencyType,
                 quantity: int):
        self.badge_id = badge_id
        self.badge_type = badge_type
        self.creation_time = creation_time
        self.currency_type = currency_type
        self.quantity = quantity
