###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from struct import pack, Struct

from PythonApp.qc_serial.model.CurrencyType import CurrencyType
from PythonApp.util.Config import Config

DUMPQ_FMT = '<B'
DUMPA_FMT = "<L"


class PayloadMessage:
    def __init__(self,
                 quantity: int):
        config = Config()
        self.currency_type = CurrencyType(int(config.get_master_config_value("PillarType")))
        self.quantity = quantity

    def __str__(self):
        return "PayloadMessage - {}".format(str(self.__dict__))

    def to_serial_payload(self):
        return pack(DUMPQ_FMT, self.currency_type.value)

    @staticmethod
    def build_payload_object(message):
        payload_struct = Struct(DUMPA_FMT)
        return PayloadMessage(*payload_struct.unpack(message))
