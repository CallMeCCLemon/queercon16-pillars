###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from PythonApp.cloud.RdsDao import RdsDao
from PythonApp.cloud.model.DatabaseUpdate import DatabaseUpdate
from PythonApp.pillar.PillarMessage import PillarMessage


class CloudOrchestrator:
    def __init__(self, rds_dao: RdsDao):
        self.rds_dao = rds_dao
        self.rds_dao.connect()

    def process_message(self, message: PillarMessage):
        update = DatabaseUpdate(
            message.badge_id,
            message.badge_type,
            message.creation_time,
            message.currency_type,
            message.quantity
        )
        self.rds_dao.write_update(update)

    def shutdown(self):
        self.rds_dao.disconnect()
