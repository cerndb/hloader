from hloader.schedule.ITransferScheduler import ITransferScheduler

__author__ = 'dstein'

class DummyScheduler(ITransferScheduler):
    def __init__(self):
        super().__init__()
