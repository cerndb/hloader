import os
import socket
import threading
import traceback
import re
import time

import paramiko
from paramiko.py3compat import u
from paramiko.ssh_exception import PasswordRequiredException, BadHostKeyException, AuthenticationException, SSHException
import requests

from hloader.entities.Transfer import Transfer

from hloader.transfer.ITransferRunner import ITransferRunner

RETURN = '\x0d'

UPDATE_WAIT_SECONDS = 10

__author__ = 'dstein'


class SSHRunner(ITransferRunner):
    """
    SSH transfer runner (authenticating using Kerberos), with output logging and REST API monitoring.
    """

    _application_id = None
    _job_id = None
    _transfer_status = Transfer.Status.WAITING

    def run(self) -> None:
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

        # create an SSH tunnel
        client = paramiko.SSHClient()

        # TODO properly configure the system host keys and the warning policy
        # Configure the connection policies.
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
            )

            channel = client.invoke_shell()

            self._communicate(channel)

            try:
                channel.close()
                client.close()
            except Exception:
                traceback.print_exc()

        except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as err:
            self._failed(message=str(err))

        except PasswordRequiredException:
            # TODO handle Kerberos not initialized exception
            print("Kerberos is not initialized")
            traceback.print_exc()
            # TODO automatically fix and restart the transfer?

        except Exception as err:
            self._failed(message=str(err))
            traceback.print_exc()

    def _communicate(self, channel) -> None:
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

        self._started()

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
        while not channel.exit_status_ready():

            if channel.recv_ready():
                stdout = channel.recv(1)
                buffer += u(stdout)

                if len(buffer):
                    split = buffer.split('\r\n')

                    if split[:-1]:
                        lines.append(split[:-1])
                        for line in split[:-1]:
                            # TODO update log with the line

                            # If the given line contains information about the tracking URL, or the job ID, extract the
                            # value. If both extracted, automatically start monitoring.
                            if "The url to track the job:" in line:
                                self._monitor_rest(line)
                            elif "Running job:" in line:
                                self._monitor_rest(line)

                    buffer = split[-1]

                    # The password input is in the same line, as the text, so the buffer is to be monitored.
                    if "Enter password:" in buffer:
                        # TODO update log
                        lines.append(buffer)
                        buffer = ''

                        # send the password
                        channel.send(os.environ.get("HLOADER_ORACLE_READER_PASS", ""))
                        channel.send(RETURN)

    def _monitor_rest(self, information: str) -> None:
        """
        Wait for the lines containing the application and job identifiers, then start the monitoring on a separate
        thread.

        :param information: Line containing the application or job id.
        """

        # Get the application ID.
        if not self._application_id:
            match = re.search(".*?The url to track the job: (.*)$", information)
            if match:
                self._tracking_url = match.group(1)
                match = re.search(".*?/(application_.*)/$", self._tracking_url)
                if match:
                    self._application_id = match.group(1)
                    print(self._application_id)

        # Get the job ID.
        if not self._job_id:
            match = re.search(".*?Running job: (.*)$", information)
            if match:
                self._job_id = match.group(1)
                print(self._job_id)

        # If both parts are known after this information, start monitoring.
        if self._application_id and self._job_id:
            rest_monitor = RESTMonitor(self._tracking_url, self._application_id, self._job_id)
            rest_monitor.start()

        return None

    def _update_log(self, source: str) -> None:
        """
        Use the @DatabaseManager to update the logs for this transfer.

        :param source: The identifier of the source for this update.
        """
        # TODO Database communication
        pass

    def _update_status(self) -> None:
        """
        Use the @DatabaseManager to update the status of this transfer and also update the status history.
        """
        # TODO Database communication
        pass

    def _failed(self, message: str="") -> None:
        """
        Call the needed methods to update the status of the transfer to FAILED.

        :param message: Message of the failure.
        """
        self._update_log()
        self._update_status()
        # TODO configure the methods

    def _started(self) -> None:
        """
        Call the needed methods to update the status of the transfer to STARTED.
        """
        # TODO configure the methods
        pass


class RESTMonitor(threading.Thread):
    """
    REST API monitoring class, to be run on a parallel thread.
    """

    def __init__(self, tracking_url: str, application_id: str, job_id: str):
        """
        Set up the monitor with the needed parameters.

        :param tracking_url: The tracking URL provided by the Sqoop output.
        :param application_id: Transfer application ID.
        :param job_id: Transfer job ID.
        """

        self._tracking_url = tracking_url
        self._application_id = application_id
        self._job_id = job_id
        threading.Thread.__init__(self)

    def run(self):
        """
        Start the REST monitoring.
         - Wait for the initialization of the REST interface.
         - After the first successful query, update the result periodically.
        """

        # Compose the REST URL and periodically update the status.
        match = re.search(".*?://(.*?)/", self._tracking_url)

        if match:
            address = match.group(1)
            job_status_url = "http://{address}/proxy/{application_id}/ws/v1/mapreduce/jobs/{job_id}/".format(
                address=address,
                application_id=self._application_id,
                job_id=self._job_id
            )

            while True:
                response = requests.get(job_status_url)

                if response.status_code == 200:
                    if response.text.count("ACCEPTED") > 2:
                        # The response is HTML and not JSON, when the job is only in the ACCEPTED stage.
                        time.sleep(1)
                        # TODO nicer handling
                    else:
                        try:
                            job_ = response.json()['job']
                            print(str(job_['state']) + ": " + str(job_['mapProgress']) + "%")

                            if job_['state'] != "RUNNING":
                                break
                            else:
                                time.sleep(UPDATE_WAIT_SECONDS)
                        except Exception:
                            if "SUCCEEDED" in response.text:
                                # The response is HTML and not JSON, when the job is only in the FINISHED stage.
                                print('SUCCEEDED')
                                break
                            else:
                                traceback.print_exc()
                else:
                    break

    def _update_log(self, source: str) -> None:
        """
        Use the @DatabaseManager to update the logs for this transfer.

        :param source: The identifier of the source for this update.
        """
        # TODO Database communication
        pass

    def _update_status(self) -> None:
        """
        Use the @DatabaseManager to update the status of this transfer and also update the status history.
        """
        # TODO Database communication
        pass
