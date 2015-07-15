from datetime import datetime


class Transfer(object):
    transfer_id = None
    job_id = None
    transfer_created = None
    transfer_start = None
    transfer_status = None
    transfer_last_update = None

    def __init__(self, _transfer, job):
        self.transfer_id = _transfer.id
        self.job_id = job.job_id
        self.transfer_created = str(datetime.now())
        self.transfer_start = str(_transfer.next_run_time)
        self.transfer_status = Transfer.Status.STARTED
        self.transfer_last_updated = str(datetime.now())

    class Status(object):
        # Status codes for transfers
        # STARTED   -> 0
        # RUNNING   -> 1
        # WAITING   -> 2
        # SUCCEEDED -> 3
        # FAILED    -> 4

        STARTED, RUNNING, WAITING, SUCCEEDED, FAILED = range(5)
