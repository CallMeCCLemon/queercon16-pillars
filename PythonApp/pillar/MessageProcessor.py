###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

import errno
import os

from PythonApp.cloud.CloudOrchestrator import CloudOrchestrator
from PythonApp.cloud.RdsDao import RdsDao
from PythonApp.cloud.model.BadgeType import BadgeType
from PythonApp.qc_serial.model.PillarType import PillarType
from PythonApp.qc_serial.model.CurrencyType import CurrencyType
from PythonApp.pillar.PillarMessage import PillarMessage
from PythonApp.pillar.PillarDao import PillarDao
from PythonApp.util.Config import Config


class MessageProcessor:
    def __init__(self,
                 rds_dao: RdsDao,
                 pillar_dao: PillarDao,
                 cloud_orchestrator: CloudOrchestrator):
        self.config = Config()
        self.pipe_name = self.config.get_pillar_config_value("PipeName")
        self.rds_dao = rds_dao
        self.q_badge_currency = 0
        self.c_badge_currency = 0
        self.pillar_type = PillarType(int(self.config.get_master_config_value("PillarType")))
        self.c_badge_target_currency = int(self.config.get_pillar_config_value("CBadgeTargetAmount"))
        self.q_badge_target_currency = int(self.config.get_pillar_config_value("QBadgeTargetAmount"))
        self.pillar_dao = pillar_dao
        self.cloud_orchestrator = cloud_orchestrator
        self.start_up()

    def start_up(self):
        # Get the current currency count from the SQL DB
        query_template = "select quantity from {} where currency_type = {}"
        df = self.rds_dao.read(
            query_template.format(
                self.rds_dao.table_name,
                self.get_q_badge_currency_type().value))
        self.q_badge_currency = df['quantity'].sum()
        print("Q Badge starting currency: {}".format(self.q_badge_currency))

        df = self.rds_dao.read(
            query_template.format(
                self.rds_dao.table_name,
                self.get_c_badge_currency_type().value))
        self.c_badge_currency = df['quantity'].sum()
        print("C Badge starting currency: {}".format(self.c_badge_currency))
        self.pillar_dao.send(str(self.calculate_message_value()))

    def process(self):
        try:
            os.mkfifo(self.pipe_name)
        except OSError as ex:
            print(ex)
            if ex.errno != errno.EEXIST:
                raise ex
        with open(self.pipe_name) as messageQueue:
            input_line = ""
            while True:
                try:
                    input_line = messageQueue.readline()
                    if len(input_line) > 0:
                        message = PillarMessage.build_message(input_line)
                        self.handle_message(message)
                except ValueError as ex:
                    print(input_line)
                    print(ex)

    def handle_message(self, message: PillarMessage):
        if message.quantity == 0:
            # self.pillar_dao.restart(self.calculate_message_value())
            return

        if message.badge_type == BadgeType.C_BADGE:
            self.c_badge_currency += message.quantity
            message.currency_type = CurrencyType(message.currency_type.value + 3)
        else:
            self.q_badge_currency += message.quantity

        payload = self.calculate_message_value()

        self.cloud_orchestrator.process_message(message)
        self.pillar_dao.write(str(payload))

    def get_q_badge_currency_type(self):
        if self.pillar_type == PillarType.PARTY:
            return CurrencyType.COINS
        elif self.pillar_type == PillarType.PRIDE:
            return CurrencyType.CAMERAS
        else:
            return CurrencyType.LOCKS

    def get_c_badge_currency_type(self):
        if self.pillar_type == PillarType.PARTY:
            return CurrencyType.COCKTAILS
        elif self.pillar_type == PillarType.PRIDE:
            return CurrencyType.FLAGS
        else:
            return CurrencyType.KEYS

    def calculate_message_value(self):
        c_badge_percent = float(self.c_badge_currency) / self.c_badge_target_currency
        q_badge_percent = float(self.q_badge_currency) / self.q_badge_target_currency

        if c_badge_percent >= 1.0 and q_badge_percent >= 1.0:
            return 49
        return int((c_badge_percent + q_badge_percent) * 49 / 2)
