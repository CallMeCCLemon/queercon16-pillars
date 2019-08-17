###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from time import sleep
from PythonApp.pillar.MessageProcessor import MessageProcessor
from PythonApp.pillar.PillarDao import PillarDao
from PythonApp.cloud.RdsDao import RdsDao
from PythonApp.cloud.CloudOrchestrator import CloudOrchestrator
from PythonApp.qc_serial.SerialUtil import SerialUtil


def main():
    # test_pillar_dao()
    showtime()


def test_pillar_dao():
    pillar_dao = PillarDao("/dev/ttyUSB0")
    print("Writing zero to pillar!")
    pillar_dao.write("0")
    sleep(5)

    print("Writing 48 to pillar!")
    pillar_dao.write("48")
    sleep(5)
    print("DONE Testing Pillar Dao")


def showtime():
    rds_dao = RdsDao()
    cloud_orch = CloudOrchestrator(rds_dao)
    port = SerialUtil.get_pillar_ports()[0]
    pillar_dao = PillarDao(port)
    print("Waiting for pillar to reset...")
    processor = MessageProcessor(rds_dao, pillar_dao, cloud_orch)
    processor.process()


if __name__ == "__main__":
    main()
