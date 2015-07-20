from __future__ import absolute_import
from datetime import datetime


class Transfer(object):
    transfer_id = None
    scheduler_transfer_id = None
    job_id = None
    transfer_start = None
    transfer_status = None
    transfer_last_update = None

    class Status(object):
        # Status class for transfers
        STARTED = "STARTED"
        RUNNING = "RUNNING"
        WAITING = "WAITING"
        SUCCEEDED = "SUCCEEDED"
        FAILED = "FAILED"
