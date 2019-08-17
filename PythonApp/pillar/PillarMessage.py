###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from datetime import datetime
from dateutil import parser

from PythonApp.cloud.model.BadgeType import BadgeType
from PythonApp.qc_serial.model.CurrencyType import CurrencyType


class PillarMessage:
    def __init__(self,
                 badge_id: int,
                 creation_time: datetime,
                 currency_type: CurrencyType,
                 quantity: int):
        self.badge_id = badge_id
        self.badge_type = BadgeType.Q_BADGE if badge_id <= 999 else BadgeType.C_BADGE
        self.creation_time = creation_time
        self.currency_type = currency_type
        self.quantity = quantity

    def to_bytes(self) -> bytes:
        return self.__repr__().encode("UTF-8")

    def __repr__(self):
        return ",".join([
            str(self.badge_id),
            str(self.creation_time.isoformat()),
            str(self.currency_type.value),
            str(self.quantity),
            ""
        ])

    @staticmethod
    def build_message(message_string):
        # message_string = message_bytes.decode("UTF-8")
        split_message = message_string.split(",")
        return PillarMessage(
            int(split_message[0]),
            parser.parse(split_message[1]),
            CurrencyType(int(split_message[2])),
            int(split_message[3]))
