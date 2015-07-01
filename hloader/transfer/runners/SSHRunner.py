from hloader.entities import Transfer
from hloader.transfer.ITransferRunner import ITransferRunner

__author__ = 'dstein'


class SSHRunner(ITransferRunner):
    def run(self, transfer : Transfer):
        self._transfer = transfer

        # prepare the sqoop command