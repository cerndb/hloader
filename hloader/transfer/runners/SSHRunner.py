import os
import socket
import traceback
import sys

import paramiko
from paramiko.ssh_exception import PasswordRequiredException

from hloader.transfer.ITransferRunner import ITransferRunner

__author__ = 'dstein'


class SSHRunner(ITransferRunner):
    def run(self):
        # TODO create a Transfer entity for the job

        # create an SSH tunnel
        client = paramiko.SSHClient()

        # TODO properly configure the system host keys and the warning policy
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        cluster = self._job.get_destination_cluster()
        hostname = socket.getfqdn(cluster.cluster_address)
        username = os.environ.get("HLOADER_HADOOP_USER", "")  # TODO

        try:
            client.connect(
                hostname,
                22,  # TODO might be different
                username,
                gss_auth=True,  # Using Kerberos authentication
                look_for_keys=False
            )

            channel = client.invoke_shell()

            # start the transfer
            channel.send(self.sqoop_command)

            # monitor the transfer
            while True:
                output = channel.recv(1024)
                if (output == 0):
                    break
                sys.stdout.write(output)
                sys.stdout.flush()

            try:
                channel.close()
                client.close()
            except Exception:
                traceback.print_exc()

        except PasswordRequiredException:
            # TODO handle Kerberos not initialized exception
            sys.stdout.write("Kerberos is not initialized")
            sys.stdout.flush()
            traceback.print_exc()
        except Exception:
            traceback.print_exc()
            raise
