###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from datetime import datetime

from PythonApp.pillar.PillarMessage import PillarMessage
from PythonApp.qc_serial.model.HeaderMessage import HeaderMessage
from PythonApp.qc_serial.model.PayloadMessage import PayloadMessage


class PillarMessageTransformer:
    @staticmethod
    def transform_serial_message_to_pillar_message(header: HeaderMessage, payload: PayloadMessage):
        return PillarMessage(
            header.from_id,
            datetime.now(),
            payload.currency_type,
            payload.quantity
        )
