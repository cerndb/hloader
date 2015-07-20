from __future__ import absolute_import

from hloader.schedule.schedulers.APScheduler import APScheduler


class SchedulerManager(object):
    daemon = None

    def __init__(self, agent):
        SchedulerManager.daemon = {
            "APScheduler": APScheduler()
        }.get(agent, None)

        SchedulerManager.daemon.start()