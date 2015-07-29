from __future__ import absolute_import

from hloader.schedule.schedulers.APScheduler import APScheduler


class ScheduleManager(object):
    daemon = None

    def __init__(self, agent):
        ScheduleManager.daemon = {
            "APScheduler": APScheduler()
        }.get(agent, None)

        ScheduleManager.daemon.start()
