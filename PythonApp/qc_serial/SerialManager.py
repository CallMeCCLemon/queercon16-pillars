###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

import serial

from PythonApp.qc_serial.SerialUtil import SerialUtil
from PythonApp.qc_serial.SerialListener import SerialListener


class SerialManager:
    def __init__(self):
        pass

    def manage_listeners(self):
        # Ensure every port name has a corresponding listener instantiated.
        currently_open_ports = SerialUtil.get_open_ports()

        print("iterating over ports")
        for port in currently_open_ports:
            try:
                SerialListener(port).listen()
            except (TimeoutError, serial.SerialException):
                pass
