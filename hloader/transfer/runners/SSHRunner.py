import os
import socket
import traceback

import paramiko
from paramiko.py3compat import u
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
                # look_for_keys=False
            )

            channel = client.invoke_shell()

            # start the transfer
            channel.send(self.sqoop_command)
            channel.send('\x0d')

            # stdin, stdout, stderr = client.exec_command(self.sqoop_command)

            # monitor the transfer
            lines = []
            output = ""

            while not channel.exit_status_ready():

                if channel.recv_ready():
                    stdout = channel.recv(1)
                    output += u(stdout)

                    if len(output):
                        split = output.split('\r\n')

                        if split[:-1]:
                            lines.append(split[:-1])
                            for line in split[:-1]:
                                print(line)
                        output = split[-1]

                        # print('output: ' + output)

                        if "Enter password:" in output:
                            lines.append(output)
                            output = ''

                            channel.send(os.environ.get("HLOADER_ORACLE_READER_PASS", ""))
                            channel.send('\x0d')

            try:
                # channel.close()
                client.close()
            except Exception:
                traceback.print_exc()

        except PasswordRequiredException:
            # TODO handle Kerberos not initialized exception
            print("Kerberos is not initialized")
            traceback.print_exc()
        except Exception:
            traceback.print_exc()
            raise
