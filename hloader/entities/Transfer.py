from enum import Enum

__author__ = 'dstein'


class Transfer:
    transfer_id = None
    job_id = None
    transfer_status = None
    transfer_start = None
    transfer_last_update = None

    class Status(Enum):
        WAITING = "waiting"
        STARTED = "started"
        SUCCEEDED = "succeeded"
        # TODO collect status values