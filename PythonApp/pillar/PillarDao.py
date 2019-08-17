###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

import serial
from time import sleep

from PythonApp.util.Config import Config


class PillarDao:
    DRIP_VALUE = "55"

    def __init__(self, port_name):
        self.config = Config()
        self.ser = serial.Serial(port=port_name,
                                 baudrate=self.config.get_pillar_config_value("BaudRate"),
                                 parity=serial.PARITY_NONE)

    def write(self, message: str):
        self.send(message)
        sleep(0.12)
        self.send(PillarDao.DRIP_VALUE)
        sleep(2.4)

    def send(self, message: str):
        for index in range(0, len(message)):
            self.ser.write(message[index].encode('ascii'))
