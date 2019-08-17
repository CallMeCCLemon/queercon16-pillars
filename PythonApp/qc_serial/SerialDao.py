###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

import serial


SYNC_BYTE = b'\xAC'


class SerialDao:
    def __init__(self,
                 port_name: str,
                 baud_rate: int,
                 timeout: int,
                 parity=serial.PARITY_NONE):
        self.ser = serial.Serial(port_name,
                                 baud_rate,
                                 parity=parity,
                                 timeout=timeout)

    def read(self, length: int):
        return self.ser.read(length)

    def write(self, message):
        self.ser.write(SYNC_BYTE)
        self.ser.write(message)

    def write_no_sync(self, message):
        self.ser.write(message)
