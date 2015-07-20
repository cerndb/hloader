from __future__ import absolute_import

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from hloader.schedule.ITransferScheduler import ITransferScheduler
from hloader.transfer.runners.SSHRunner import SSHRunner

import logging
logging.basicConfig()


class APScheduler(ITransferScheduler):
    transfer_instance = None

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

    def start(self):
        print "Starting the scheduling daemon"
        self.scheduler.start()

    def load_job(self, job, trigger, **kwargs):
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
        """
        APScheduler.transfer_instance = self.scheduler.add_job(tick, trigger, [job], **kwargs)

    def remove_transfer(self, scheduler_transfer_id):
        """
        Remove a transfer, and prevent it from being run any more.
        :param scheduler_transfer_id: Transfer ID used by the scheduler in its job store
        """
        self.scheduler.remove_job(job_id=scheduler_transfer_id)

    def pause_transfer(self, scheduler_transfer_id):
        """
        Cause the given transfer not to be executed until it is explicitly resumed.
        :param scheduler_transfer_id: Transfer ID used by the scheduler in its job store
        """
        self.scheduler.pause_job(job_id=scheduler_transfer_id)

    def resume_transfer(self, scheduler_transfer_id):
        """
        Resumes the schedule of the given transfer.
        :param scheduler_transfer_id: Transfer ID used by the scheduler in its job store
        """
        self.scheduler.resume_job(job_id=scheduler_transfer_id)


# For serialising the Job and getting a textual reference to the function, we need to keep it outside any class

def tick(job):
    runner = SSHRunner(job, APScheduler.transfer_instance)
    runner.run()
