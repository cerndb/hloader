#from __future__ import absolute_import
import threading
import time

__author__ = 'dstein'


class ITransferScheduler(object, threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(10*60)
        pass