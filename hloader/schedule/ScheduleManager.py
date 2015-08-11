from __future__ import absolute_import

from hloader.schedule.schedulers.APScheduler import APScheduler
from hloader.db.DatabaseManager import DatabaseManager

import threading
import time


class ScheduleManager(object):
    daemon = None

    def __init__(self, agent):
        ScheduleManager.daemon = {
            "APScheduler": APScheduler()
        }.get(agent, None)

        ScheduleManager.daemon.start()


class HLoaderAgent(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.SM = ScheduleManager('APScheduler')
        self.polling_factor = 10

    def run(self):
        while True:
            self.busy_wait()

            touched_jobs = DatabaseManager.meta_connector.get_recently_touched_jobs(polling_factor=self.polling_factor)

            if not touched_jobs:
                print("[Agent] Found no touched Jobs\n")

            for job in touched_jobs:
                most_recent_transfer = DatabaseManager.meta_connector.get_transfers(
                    job_id=job.job_id, order='transfer_id')

                if most_recent_transfer:
                    print("[Agent] Job modification detected")
                    # A Job existing in the local jobstore was modified
                    if not job.interval:
                        self.SM.daemon.modify_job(job, 'date', run_date=job.start_time)
                    else:
                        self.SM.daemon.modify_job(job, 'interval', seconds=job.interval.seconds)
                else:
                    print("[Agent] New Job detected")
                    # New Job detected
                    if not job.interval:
                        self.SM.daemon.load_job(job, 'date', run_date=job.start_time)
                    else:
                        self.SM.daemon.load_job(job, 'interval', seconds=job.interval.seconds)

    def busy_wait(self):
            time.sleep(self.polling_factor)
