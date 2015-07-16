from __future__ import absolute_import
from datetime import datetime
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from hloader.entities.Transfer import Transfer
from hloader.entities.Job import Job

import logging
logging.basicConfig()


class APScheduler(object):
    def __init__(self):
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
        self.scheduler = BackgroundScheduler(jobstores=settings['jobstore'],
                                             executors=settings['executors'],
                                             job_defaults=settings['job_defaults'],
                                             timezone=settings['timezone'])

        print "Starting the scheduling daemon"
        self.scheduler.start()


def start_transfer(aps, job, trigger, **kwargs):
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
    _transfer = aps.scheduler.add_job(tick, trigger, **kwargs)
    # transfer = Transfer(job, _transfer)


def tick():
    # This is dummy job
    print 'Tick! The time is: %s' % datetime.now()


if __name__ == '__main__':
    # Wait for 5 seconds and start the scheduler
    time.sleep(5)
    aps_obj = APScheduler()

    start_transfer(aps_obj, None, 'interval', seconds=2)
    while True:
        # TODO: Fine tune this setting to decrease CPU busy waiting
        time.sleep(60)
