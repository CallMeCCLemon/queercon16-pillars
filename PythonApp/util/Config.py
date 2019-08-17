###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

from configparser import ConfigParser


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.master_key = "Master"
        self.serial_key = "Serial"
        self.pillar_key = "Pillar"

    def get_master_config_value(self, config_key: str):
        return self.config[self.master_key][config_key]

    def get_serial_config_value(self, config_key: str):
        return self.config[self.serial_key][config_key]

    def get_pillar_config_value(self, config_key: str):
        return self.config[self.pillar_key][config_key]
