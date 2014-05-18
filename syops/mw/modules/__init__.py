import threading
import time

class Abstract(threading.Thread):

    def __init__(self):
        super(Abstract, self).__init__()
        self.daemon = True
        self.is_running = True

        # Default to running every 5 seconds
        self._interval = 5
        self._last_run = None

    def init(self):
        pass

    def loop(self):
        pass

    def cleanup(self):
        self.is_running = False

    def run(self):
        self.init()

        while self.is_running:
            if not self._last_run or (time.time() > self._last_run + self._interval):
                self.loop()
                self._last_run = time.time()

            time.sleep(1)
