###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from enum import Enum

from PythonApp.pillar.MessageClient import MessageClient
from PythonApp.pillar.PillarMessageTransformer import PillarMessageTransformer
from PythonApp.qc_serial.SerialDao import SerialDao
from PythonApp.qc_serial.SerialUtil import SerialUtil
from PythonApp.qc_serial.model.HeaderMessage import HeaderMessage
from PythonApp.qc_serial.model.OpCode import OpCode
from PythonApp.qc_serial.model.PayloadMessage import PayloadMessage
from PythonApp.util.Config import Config


class States(Enum):
    DISCONNECTED = 0
    CONNECTED = 1


class SerialStateMachine:
    def __init__(self, serial_dao: SerialDao):
        self.active_state = States.DISCONNECTED
        self.config = Config()
        self.states = {
            States.DISCONNECTED: self.disconnected,
            States.CONNECTED: self.connected,
        }
        self.serial_dao = serial_dao
        self.message_client = MessageClient()

        self.header_message_length = 11
        self.done = False

    def run(self):
        while not self.done:
            self.states[self.active_state]()

    def disconnected(self):
        # Send HELO Messages waiting for an ACK.You
        hello_message = HeaderMessage(
            OpCode.HELO,
            0,
            int(self.config.get_master_config_value("PillarID")),
            0)

        self.serial_dao.write(hello_message.to_serial_payload())
        message = self.serial_dao.read(self.header_message_length)

        try:
            SerialUtil.validate_message_header(message)
        except TimeoutError as ex:
            return
        except ValueError as ex:
            print(ex)
            return

        header_message = HeaderMessage.build_header_object(message[1:])
        if header_message.opcode == OpCode.ACK:
            print("Received ACK! Now connected to badge {}!".format(header_message.from_id))
            self.active_state = States.CONNECTED
        else:
            print("Received unknown message! Skipping..")

    def connected(self):
        # Send DUMPQ messages waiting for a DUMPA.
        dump_q_message = HeaderMessage(
            OpCode.DUMPQ,
            1,
            int(self.config.get_master_config_value("PillarID")),
            0)
        dump_q_payload = PayloadMessage(int(self.config.get_master_config_value("PillarType")))
        print("Sending dump Q message!")
        print("Dump Q Header: {}".format(dump_q_message.to_serial_payload(dump_q_payload)))
        self.serial_dao.write(dump_q_message.to_serial_payload(dump_q_payload))
        print("Dump q payload: {}".format(dump_q_payload.to_serial_payload()))
        self.serial_dao.write_no_sync(dump_q_payload.to_serial_payload())

        message = self.serial_dao.read(self.header_message_length)
        try:
            SerialUtil.validate_message_header(message)
            header_message = HeaderMessage.build_header_object(message[1:])
            if header_message.opcode == OpCode.DUMPA:
                print("Received DUMPA! Sending update to cloud!")
                message = self.serial_dao.read(header_message.payload_len)
                payload_message = PayloadMessage.build_payload_object(message)
                pillar_message = PillarMessageTransformer\
                    .transform_serial_message_to_pillar_message(header_message, payload_message)
                self.message_client.send_message_to_queue(pillar_message)
                self.done = True
            else:
                print("Unexpected message type!")
        except TimeoutError as ex:
            print(ex)
        except ValueError as ex:
            print(ex)

        self.active_state = States.DISCONNECTED
