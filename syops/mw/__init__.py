import threading
import logging
from time import sleep

from syops.lib.application import Application
from syops.mw.modules.releases import Releases

class Syops(threading.Thread):

    def __init__(self):
        super(Syops, self).__init__()
        Application.bootstrap()
        self.is_running = True

        # Setup modules to be run
        self.modules = [
            Releases()
        ]

    def run(self):
        logging.info('Syops is starting...')
        for module in self.modules:
            module.start()

        while self.is_running:
            sleep(1)

    def stop(self):
        logging.info('Syops is shutting down...')
        self.is_running = False
        for module in self.modules:
            module.cleanup()
