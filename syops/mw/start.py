#!/home/david/projects/syops/env/bin/python
import signal
import sys

from syops.mw import Syops

syops = None

def signal_handler(signal, frame):
    if syops:
        syops.stop()

if __name__ == "__main__":
    # Setup our signal handler to stop the applicaiton gracefully
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    syops = Syops()
    syops.start()
    signal.pause() # sleep until signal is caught
