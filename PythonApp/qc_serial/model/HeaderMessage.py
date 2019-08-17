###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from struct import pack, Struct

from PythonApp.qc_serial.CrcHandler import CrcHandler
from PythonApp.qc_serial.model.OpCode import OpCode
from PythonApp.qc_serial.model.PayloadMessage import PayloadMessage

HEADER_FMT_NOCRCs = '<BBHH'
HEADER_FMT = '<BBHHHH'
CRC_FMT = '<H'


class HeaderMessage:
    def __init__(
            self,
            opcode,
            payload_len,
            from_id,
            to_id,
            payload_crc=None,
            header_crc=None,
            payload: PayloadMessage = None):
        self.opcode = OpCode(opcode)
        self.payload_len = payload_len
        self.from_id = from_id
        self.to_id = to_id
        if payload_crc and payload:
            assert CrcHandler.calculate_crc16(payload.to_serial_payload()) == payload_crc, "Invalid Payload CRC!!"
        if header_crc and payload_crc:
            message = pack(
                HEADER_FMT_NOCRCs,
                self.opcode.value,
                self.payload_len,
                self.from_id,
                self.to_id)
            message += pack(CRC_FMT, payload_crc)
            assert CrcHandler.calculate_crc16(message) == header_crc, "Invalid Header CRC!!"

    def __str__(self):
        return "HeaderMessage - {}".format(str(self.__dict__))

    def to_serial_payload(self, payload: PayloadMessage = None):
        message = pack(
            HEADER_FMT_NOCRCs,
            self.opcode.value,
            self.payload_len,
            self.from_id,
            self.to_id)
        message += pack(CRC_FMT, CrcHandler.calculate_crc16(payload.to_serial_payload()) if payload else 0x00)
        message += pack(CRC_FMT, CrcHandler.calculate_crc16(message))
        return message

    @staticmethod
    def build_header_object(message):
        header_struct = Struct(HEADER_FMT)
        return HeaderMessage(*header_struct.unpack(message))
