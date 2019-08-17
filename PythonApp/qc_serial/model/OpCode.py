###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from enum import Enum


class OpCode(Enum):
    HELO = 0x01
    ACK = 0x02
    ELEMENT = 0x03
    STAT1Q = 0x04
    STAT2Q = 0x05
    STATA = 0x06
    PUTFILE = 0x09
    APPFILE = 0x0A
    ENDFILE = 0x0B
    SETID = 0x0C
    SETNAME = 0x0D
    DUMPQ = 0x0E
    DUMPA = 0x0F
    DISCON = 0x10
    SETTYPE = 0x11
    PAIR = 0x12
    GETFILE = 0x13
    GOMISSION = 0x14
