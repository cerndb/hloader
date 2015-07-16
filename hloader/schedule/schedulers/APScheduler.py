from __future__ import absolute_import
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from hloader.transfer.runners.SSHRunner import SSHRunner

import logging
logging.basicConfig()


class APScheduler(object):
    scheduler = None
    aps_transfer = None

    @staticmethod
    def init():
        settings = {
            'jobstore': {
                # Keep the schedule information in an encrypted SQLite local store.
                'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
            },

            # TODO: Avoid hardcoding ThreadPoolExecutor and ProcessPoolExecutor
            'executors': {
                'default': ThreadPoolExecutor(20),
                'processpool': ProcessPoolExecutor(5)
            },

            'job_defaults': {
                # TODO: Investigate if we need to coalesce missed jobs
                'coalesce': False,
                'max_instances': 3
            },

            'timezone': "Europe/Zurich"
        }

        print "Initializing APScheduler"
        APScheduler.scheduler = BackgroundScheduler(jobstores=settings['jobstore'],
                                                    executors=settings['executors'],
                                                    job_defaults=settings['job_defaults'],
                                                    timezone=settings['timezone'])

        print "Starting the scheduling daemon"
        APScheduler.scheduler.start()

    @staticmethod
    def load_job(job, trigger, **kwargs):
        """
        Start a new transfer for a given job.

        Accepted values of trigger: [date | interval | cron]
        Refer to the API reference of APScheduler for details about trigger
        parameters.

        date: apscheduler.triggers.date
        interval: apscheduler.triggers.interval
        cron: apscheduler.triggers.cron

        :param aps: Instance of the class APScheduler
        :param job: Instance of the Job entity
        :param trigger: Type of trigger for the transfer
        :param kwargs: Trigger specific parameters
        :return: Transfer instance
        """
        APScheduler.aps_transfer = APScheduler.scheduler.add_job(tick, trigger, [job], **kwargs)


# For serialising the Job and getting a textual reference to the function, we need to keep it outside any class

def tick(job):
    runner = SSHRunner(job, APScheduler.aps_transfer)
    runner.run()


if __name__ == '__main__':
    # Wait for 5 seconds and start the scheduler
    time.sleep(5)
    aps_obj = APScheduler()
    aps_obj.init()

    aps_obj.load_job('foo', 'interval', seconds=5)
    while True:
        # TODO: Fine tune this setting to decrease CPU busy waiting
        time.sleep(60)
