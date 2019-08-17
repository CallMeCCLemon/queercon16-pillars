###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

import os

from PythonApp.pillar.PillarMessage import PillarMessage
from PythonApp.util.Config import Config


class MessageClient:
    def __init__(self):
        self.config = Config()
        self.pipe_name = self.config.get_pillar_config_value("PipeName")

    def send_message_to_queue(self, message: PillarMessage):
        print("New message: {}".format(message))
        pipe = os.open(self.pipe_name, os.O_WRONLY)
        os.write(pipe, message.to_bytes())
        os.close(pipe)
