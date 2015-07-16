from __future__ import absolute_import
from hloader.db.DatabaseManager import DatabaseManager

__author__ = 'dstein'

from hloader.schedule.schedulers.DummyScheduler import DummyScheduler

class SchedulerManager(object):
    _scheduler = DummyScheduler()

    def __init__(self):
        super(SchedulerManager, self).__init__()

    def run(self):
        SchedulerManager._scheduler.start()
