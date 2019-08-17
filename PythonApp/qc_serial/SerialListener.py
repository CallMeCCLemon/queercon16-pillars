###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

import threading

from PythonApp.qc_serial.SerialDao import SerialDao
from PythonApp.qc_serial.SerialStateMachine import SerialStateMachine
from PythonApp.util.Config import Config


class SerialListener:
    """
        Responsible for listening to serial messages which are incoming through the port the given listener is assigned
        to. When the port the listener is responsible for is closed, the process should exit.
    """

    def __init__(self, port_name: str):
        self.config = Config()
        self.baud_rate = self.config.get_serial_config_value("BaudRate")
        self.port_name = port_name
        self.serial_dao = SerialDao(
            self.port_name,
            int(self.config.get_serial_config_value("BaudRate")),
            int(self.config.get_serial_config_value("SerialTimeout")))
        self.state_machine = SerialStateMachine(self.serial_dao)

    def listen(self):
        print("Listening".format(self.port_name))
        timer = threading.Timer(
            2.0 * float(self.config.get_serial_config_value("SerialTimeout")),
            self.exception)
        timer.start()
        self.state_machine.run()
        timer.cancel()

    def exception(self):
        raise TimeoutError("Timeout reached: Aborting process!")
