#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
import os
import socket
import traceback
import re

import paramiko
from paramiko.py3compat import u

from paramiko.ssh_exception import PasswordRequiredException, BadHostKeyException, AuthenticationException, SSHException

from hloader.db.DatabaseManager import DatabaseManager
from hloader.entities.Transfer import Transfer
from hloader.transfer.ITransferRunner import ITransferRunner
from hloader.transfer.monitors.RESTMonitor import RESTMonitor
from hloader.entities.Log import Log

RETURN = '\x0d'

__author__ = 'dstein'


class SSHRunner(ITransferRunner):
    """
    SSH transfer runner (authenticating using Kerberos), with output logging and REST API monitoring.

    :type _transfer: Transfer
    :type _ssh_log: Log
    """

    _application_id = None
    _job_id = None
    _transfer_status = Transfer.Status.WAITING
    _transfer = None
    _ssh_log = None

    def run(self):
        """
        Run a new transfer for the job it was initialized with.

         - Create a @Transfer entity.
         - Initialize the SSH tunnel.
         - Send the Sqoop command.
           - Send the password when needed.
           - Log every output line, if it contains tracking information, start the REST monitoring.
             - Wait for the initialization of the REST interface.
             - After the first successful query, update the result periodically.
        """

        # TODO create a Transfer entity for the job
        self._transfer = self.transfer
        self._ssh_log = DatabaseManager.meta_connector.get_log(self._transfer, "SSH")


        # create an SSH tunnel
        client = paramiko.SSHClient()

        # TODO properly configure the system host keys and the warning policy
        # Configure the connection policies.
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())

        cluster = DatabaseManager.meta_connector.get_clusters(cluster_id=self._job.destination_cluster_id)[0]
        hostname = socket.getfqdn(cluster.cluster_address)
        username = os.environ.get("HLOADER_HADOOP_USER", "")  # TODO

        try:
            client.connect(
                hostname,
                22,  # TODO might be different
                username,
                gss_auth=True,  # Using Kerberos authentication
            )

            channel = client.invoke_shell()

            self._communicate(channel)

            try:
                channel.close()
                client.close()
            except Exception as err:
                # TODO: Too broad exception clause
                traceback.print_exc()
                raise err

        except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as err:
            self._transfer_failed(message=str(err))
            traceback.print_exc()
            raise err

        except PasswordRequiredException as err:
            # TODO handle Kerberos not initialized exception
            print("Kerberos is not initialized")
            traceback.print_exc()
            # TODO automatically fix and restart the transfer?
            raise err

        except Exception as err:
            self._transfer_failed(message=str(err))
            traceback.print_exc()
            raise err

    def _communicate(self, channel):
        """
        Use the SSH tunnel to start the transfer.

         - Send the Sqoop command.
           - Send the password when needed.
           - Log every output line, if it contains tracking information, start the REST monitoring.
             - Wait for the initialization of the REST interface.
             - After the first successful query, update the result periodically.

        If there is an exception, the caller has to handle it.

        :param channel: SSH tunnel that had been set up.
        """

        self._transfer_started()

        # start the transfer
        channel.send(self.sqoop_command)
        channel.send(RETURN)

        # The byte/character output has to be processed one-by-one, as the password prompt does not return the line, and
        # bigger buffer size could leave the whole session hanging, as there would be no more output sent, before the
        # password is sent.
        lines = []
        buffer = ""

        # Monitor the transfer
        # Since the Sqoop command ends with exit, the channel will also quit after the transfer finished.
        # TODO after the password is sent, the buffer size can be higher (AIMD)

        """:type : Log"""

        buffersize = 1
        buffersize_max = 1024
        password_sent = False

        channel.settimeout(1.0)

        while not channel.exit_status_ready():
            try:
                if channel.recv_ready():
                    stdout = channel.recv(buffersize)
                    buffer += u(stdout)

                    # print("buf " + str(buffersize) + " -- " + buffer)

                    if len(buffer):
                        # AIMD AI
                        if buffersize < buffersize_max:
                            buffersize += 1

                        split = buffer.split('\r\n')

                        if split[:-1]:
                            for line in split[:-1]:
                                lines.append(line)
                                print(line)
                                # If the given line contains information about the tracking URL, or the job ID,
                                # extract the value. If both extracted, automatically start monitoring.
                                if "The url to track the job:" in line:
                                    self._monitor_rest(line)
                                elif "Running job:" in line:
                                    self._monitor_rest(line)

                            # TODO Not optimal solution, not incremental.
                            self._update_log("\n".join(lines))

                        buffer = split[-1]

                        # The password input is in the same line, as the text, so the buffer is to be monitored.
                        if "Enter password:" in buffer:
                            # TODO update log (? if needed, now it does not contain the password prompt)
                            lines.append(buffer)
                            buffer = ''

                            # send the password
                            channel.send(os.environ.get("HLOADER_ORACLE_READER_PASS", ""))
                            channel.send(RETURN)

                    else:
                        # AIMD MD
                        buffersize = max(buffersize / 2, 1)
            except socket.timeout as err:
                buffersize = max(buffersize / 2, 1)
                traceback.print_exc()
                raise err

    def _monitor_rest(self, information):
        """
        Wait for the lines containing the application and job identifiers, then start the monitoring on a separate
        thread.

        :param information: Line containing the application or job id.

        :type information: str

        :return: None
        """

        # Get the application ID.
        if not self._application_id:
            match = re.search(".*?The url to track the job: (.*)$", information)
            if match:
                self._tracking_url = match.group(1)
                match = re.search(".*?/(application_.*)/$", self._tracking_url)
                if match:
                    self._application_id = match.group(1)
                    # print(self._application_id)

        # Get the job ID.
        if not self._job_id:
            match = re.search(".*?Running job: (.*)$", information)
            if match:
                self._job_id = match.group(1)
                # print(self._job_id)

        # If both parts are known after this information, start monitoring.
        if self._application_id and self._job_id:
            rest_monitor = RESTMonitor(self._tracking_url, self._application_id, self._job_id)
            rest_monitor.start()

        return None

    def _update_log(self, content):
        """
        Use the @DatabaseManager to update the logs for this transfer.

        :param content: The content of the log to be saved.

        :type content:  str

        :return None
        """
        self._ssh_log.log_content = content
        DatabaseManager.meta_connector.save_log(self._ssh_log)

        return None

    def _update_status(self, status):
        """
        Use the @DatabaseManager to update the status of this transfer and also update the status history.

        :param status: The updated status message.

        :type status: str

        :return: None
        """
        DatabaseManager.meta_connector.modify_status(self._transfer, status)

        return None

    def _transfer_failed(self, message=""):
        """
        Call the needed methods to update the status of the transfer to FAILED.

        :param message: Message of the failure.

        :type message: str

        :return None
        """
        # self._update_log()
        self._update_status("FAILED")
        # TODO configure the methods

    def _transfer_started(self):
        """
        Call the needed methods to update the status of the transfer to STARTED.
        """
        self._update_status("RUNNING")
