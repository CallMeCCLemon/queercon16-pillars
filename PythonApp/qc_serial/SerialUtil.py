###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

import sys
import glob

SYNC_BYTE = 0xAC


class SerialUtil:
    @staticmethod
    def get_pillar_ports():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/ttyACM*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.usbmodem*')
        else:
            raise EnvironmentError('Unsupported platform')

        return ports

    @staticmethod
    def get_open_ports():
        """
            Lists serial port names
            Credit: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/ttyUSB*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.usbserial*')
        else:
            raise EnvironmentError('Unsupported platform')

        # for port in ports:
        #     try:
        #         s = serial.Serial(port)
        #         s.close()
        #         result.append(port)
        #     except (OSError, serial.SerialException):
        #         pass
        return ports

    @staticmethod
    def validate_message_header(header):
        if len(header) < 11:
            raise TimeoutError("No response from badge!")
        if header[0] != SYNC_BYTE:
            raise ValueError("Bad Sync byte!!")
