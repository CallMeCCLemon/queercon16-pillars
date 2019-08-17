###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

QC16_CRC_SEED = 0xB68F


class CrcHandler:
    @staticmethod
    def calculate_crc16(sbuf):
        crc = QC16_CRC_SEED

        for b in sbuf:
            crc = (0xFF & (crc >> 8)) | ((crc & 0xFF) << 8)
            crc ^= b
            crc ^= (crc & 0xFF) >> 4
            crc ^= 0xFFFF & ((crc << 8) << 4)
            crc ^= ((crc & 0xff) << 4) << 1

        return crc
