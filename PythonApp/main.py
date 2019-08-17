###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from datetime import datetime

from PythonApp.cloud.RdsDao import RdsDao
from PythonApp.cloud.model.BadgeType import BadgeType
from PythonApp.cloud.model.DatabaseUpdate import DatabaseUpdate
from PythonApp.pillar.MessageClient import MessageClient
from PythonApp.pillar.MessageProcessor import MessageProcessor
from PythonApp.pillar.PillarMessage import PillarMessage
from PythonApp.qc_serial.SerialListener import SerialListener
from PythonApp.qc_serial.SerialManager import SerialManager
from PythonApp.qc_serial.model.CurrencyType import CurrencyType
from PythonApp.qc_serial.model.HeaderMessage import HeaderMessage
from PythonApp.qc_serial.model.OpCode import OpCode
from PythonApp.qc_serial.model.PayloadMessage import PayloadMessage
from PythonApp.util.Config import Config


def main():
    print("Starting Serial Manager")
    manager = SerialManager()
    while True:
        try:
            print("Managing listeners")
            manager.manage_listeners()
        except Exception as ex:
            print("Unexpected exception: {}".format(ex))
    # test_message_sender()
    # print(SerialUtil.get_open_ports())
    # pillar = PillarDao("/dev/tty.usbmodem14401")
    # sleep(3)
    # for i in range(0, 49):
    #     pillar.write(str(i))
    # test_calculate_message()
    # pillar.write("30")
    # pillar.write("0")
    # pillar.write("10")


def test_calculate_message():
    q = 0.0
    c = 0.0
    print(MessageProcessor.calculate_message_value(c, q))
    print("Hello")


def test_message_sender():
    client = MessageClient()
    dummy_message = PillarMessage(0, datetime.now(), CurrencyType.CAMERAS, 5)
    while True:
        client.send_message_to_queue(dummy_message)


def test_db_read():
    dao = RdsDao()
    dao.connect()
    print(dao.read('select * from badge_messages'))
    dao.disconnect()


def test_db_update():
    update = DatabaseUpdate(0, BadgeType.Q_BADGE, CurrencyType.COINS, 5)
    dao = RdsDao()
    dao.connect()
    dao.write_update(update)
    dao.disconnect()


def test_config():
    config = Config()
    print(config.get_master_config_value("PillarType"))


def test_serial_message_builder():
    header = HeaderMessage(OpCode.HELO, 0, 2, 5, 0, 0)
    header_message = header.to_serial_payload()
    print(header_message)

    payload = PayloadMessage(4)
    payload_message = payload.to_serial_payload()
    print(payload_message)

    print(header.to_serial_payload(payload))


def test_serial_listener(port):
    SerialListener(port).listen()


if __name__ == "__main__":
    main()
