from __future__ import absolute_import
from __future__ import print_function

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler import events

from hloader.schedule.ITransferScheduler import ITransferScheduler
from hloader.transfer.runners.SSHRunner import SSHRunner
from hloader.db.DatabaseManager import DatabaseManager
from hloader.db.connectors.sqlaentities.Transfer import Transfer

import threading
import Queue
import logging

logging.basicConfig()


class APScheduler(ITransferScheduler):
    scheduler = None
    mutex = threading.Lock()

    def __init__(self):
        self.settings = {
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
                'max_instances': 1
            },

            'timezone': "Europe/Zurich"
        }

        print("[Schedule Manager] Initializing APScheduler")
        APScheduler.scheduler = BackgroundScheduler(jobstores=self.settings['jobstore'],
                                                    executors=self.settings['executors'],
                                                    job_defaults=self.settings['job_defaults'],
                                                    timezone=self.settings['timezone'])

        print("[Schedule Manager] Listening to all Transfer events")
        APScheduler.scheduler.add_listener(self.event_listener, events.EVENT_ALL)
        # TODO call to super __init__ ?

    def start(self):
        APScheduler.scheduler.start()

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

        # Mutex implementation to add atomicity to the below operations.
        APScheduler.mutex.acquire()

        transfer_instance = APScheduler.scheduler.add_job(func=tick, trigger=trigger, args=[job], **kwargs)
        DatabaseManager.meta_connector.create_transfer(job, transfer_instance.id)

        APScheduler.mutex.release()

    def modify_job(self, job, trigger, **kwargs):
        # Mutex implementation to add atomicity to the below operations.
        APScheduler.mutex.acquire()

        scheduler_transfer_id = DatabaseManager.meta_connector.get_transfers(job_id=job.job_id)[0].scheduler_transfer_id
        APScheduler.scheduler.modify_job(job_id=scheduler_transfer_id, func=tick, trigger=trigger, args=[job], **kwargs)

        APScheduler.mutex.release()


    def get_scheduler_transfers(self):
        return [each.id for each in APScheduler.scheduler.get_jobs()]

    @staticmethod
    def remove_transfer(scheduler_transfer_id):
        """
        Remove a transfer, and prevent it from being run any more.
        :param scheduler_transfer_id: Transfer ID used by the scheduler in its job store
        """
        APScheduler.scheduler.remove_job(job_id=scheduler_transfer_id)

    def pause_transfer(self, scheduler_transfer_id):
        """
        Cause the given transfer not to be executed until it is explicitly resumed.
        :param scheduler_transfer_id: Transfer ID used by the scheduler in its job store
        """
        APScheduler.scheduler.pause_job(job_id=scheduler_transfer_id)

    def resume_transfer(self, scheduler_transfer_id):
        """
        Resumes the schedule of the given transfer.
        :param scheduler_transfer_id: Transfer ID used by the scheduler in its job store
        """
        APScheduler.scheduler.resume_job(job_id=scheduler_transfer_id)

    def event_listener(self, event):
        if event.code is events.EVENT_SCHEDULER_START:
            print("[Schedule Manager] The scheduling daemon was started")

        elif event.code is events.EVENT_SCHEDULER_SHUTDOWN:
            print("[Schedule Manager] The scheduling daemon was shutdown")

        elif event.code is events.EVENT_ALL_JOBS_REMOVED:
            print("[Schedule Manager] All transfers were removed from the local job store")

        elif event.code is events.EVENT_JOB_ADDED:
            print("[Schedule Manager] New transfer added to local job store")
            print("[Schedule Manager] Scheduler Transfer ID: ", event.job_id)

        elif event.code is events.EVENT_JOB_REMOVED:
            print("[Schedule Manager] Transfer removed from the local job store")
            print("[Schedule Manager] Scheduler Transfer ID: ", event.job_id)

        elif event.code is events.EVENT_JOB_MODIFIED:
            print("[Schedule Manager] Transfer modified from outside the scheduler")
            print("[Schedule Manager] Scheduler Transfer ID: ", event.job_id)

        elif event.code is events.EVENT_JOB_EXECUTED:
            APScheduler.mutex.acquire()

            print("[Schedule Manager] Transfer was executed successfully")
            print("[Schedule Manager] Scheduler Transfer ID: ", event.job_id)

            transfer = DatabaseManager.meta_connector.get_transfers(scheduler_transfer_id=event.job_id)[-1]
            DatabaseManager.meta_connector.modify_status(transfer, Transfer.Status.SUCCEEDED)

            transfer_instance = APScheduler.scheduler.get_job(event.job_id)
            if transfer_instance:
                # The Transfer is probably being triggered by an "interval". Create a new transfer with:
                #   - the same Job ID
                #   - the same Scheduler Transfer ID
                #   - WAITING status, until changed by some other event listener

                job = DatabaseManager.meta_connector.get_jobs(job_id=transfer.job_id)[0]
                DatabaseManager.meta_connector.create_transfer(job, transfer.scheduler_transfer_id)

            APScheduler.mutex.release()

        elif event.code is events.EVENT_JOB_ERROR:
            APScheduler.mutex.acquire()

            transfer = DatabaseManager.meta_connector.get_transfers(scheduler_transfer_id=event.job_id)[-1]
            DatabaseManager.meta_connector.modify_status(transfer, Transfer.Status.FAILED)
            print("[Schedule Manager] Transfer raised an exception during execution")
            print("[Schedule Manager] Scheduler Transfer ID: ", event.job_id)

            APScheduler.mutex.release()

        elif event.code is events.EVENT_JOB_MISSED:
            print("[Schedule Manager] Transfer missed")

        else:
            print("[Schedule Manager] Unknown event")


# For serialising the Job and getting a textual reference to the function, we need to keep it outside any class

def tick(job):
    APScheduler.mutex.acquire()

    if not DatabaseManager.meta_connector.get_jobs(job_id=job.job_id):
        APScheduler.remove_transfer(DatabaseManager
                                    .meta_connector
                                    .get_transfers(job_id=job.job_id, order='transfer_id')[-1]
                                    .scheduler_transfer_id)

        raise Exception("[Schedule Manager] Job doesn't exist")

    error_bucket = Queue.Queue()

    transfer = DatabaseManager.meta_connector.get_transfers(job_id=job.job_id)[-1]
    DatabaseManager.meta_connector.modify_status(transfer, Transfer.Status.RUNNING)
    runner = SSHRunner(job, transfer, error_bucket)

    APScheduler.mutex.release()

    runner.start()

    runner.join()

    # Send a EVENT_JOB_ERROR signal to the event listener if spawned thread returned after raising an exception
    try:
        exc = error_bucket.get(block=False)
    except Queue.Empty:
        pass
    else:
        exc_type, exc_obj, exc_trace = exc
        raise Exception(exc_obj)
