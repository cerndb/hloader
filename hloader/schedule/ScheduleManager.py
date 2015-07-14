from hloader.db.DatabaseManager import DatabaseManager

__author__ = 'dstein'

from hloader.schedule.schedulers.DummyScheduler import DummyScheduler

class SchedulerManager:
    _scheduler = DummyScheduler()

    def __init__(self):
        super().__init__()

    def run(self):
        SchedulerManager._scheduler.start()
