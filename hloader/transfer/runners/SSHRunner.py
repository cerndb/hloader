import os
import socket
import threading
import traceback
import re
import time

import paramiko
from paramiko.py3compat import u
from paramiko.ssh_exception import PasswordRequiredException
import requests

from hloader.transfer.ITransferRunner import ITransferRunner

__author__ = 'dstein'


class SSHRunner(ITransferRunner):
    _application_id = None
    _job_id = None

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
            )

            channel = client.invoke_shell()

            # start the transfer
            channel.send(self.sqoop_command)
            channel.send('\x0d')

            # monitor the transfer
            lines = []
            buffer = ""

            while not channel.exit_status_ready():

                if channel.recv_ready():
                    stdout = channel.recv(1)
                    buffer += u(stdout)

                    if len(buffer):
                        split = buffer.split('\r\n')

                        if split[:-1]:
                            lines.append(split[:-1])
                            for line in split[:-1]:
                                print(line)
                                if "The url to track the job:" in line:
                                    self.monitor(line)
                                elif "Running job:" in line:
                                    self.monitor(line)
                                    # channel.send('\x03')
                        buffer = split[-1]

                        # The password input is in the same line, as the text, so the buffer is to be monitored.
                        if "Enter password:" in buffer:
                            lines.append(buffer)
                            buffer = ''

                            channel.send(os.environ.get("HLOADER_ORACLE_READER_PASS", ""))
                            channel.send('\x0d')

            try:
                channel.close()
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

    def monitor(self, information:str) -> None:
        """
        Wait for the lines containing the application and job identifiers, then start the monitoring on a separate thread.
        :param information: line containing the application or job id
        """

        if not self._application_id:
            match = re.search(".*?The url to track the job: (.*)$", information)
            if match:
                self._tracking_url = match.group(1)
                match = re.search(".*?/(application_.*)/$", self._tracking_url)
                if match:
                    self._application_id = match.group(1)
                    print(self._application_id)

        if not self._job_id:
            match = re.search(".*?Running job: (.*)$", information)
            if match:
                self._job_id = match.group(1)
                print(self._job_id)

        if self._application_id and self._job_id:
            rest_monitor = RESTMonitor(self._tracking_url, self._application_id, self._job_id)
            rest_monitor.start()
            print("Starting REST monitoring")

        return None


class RESTMonitor(threading.Thread):
    def __init__(self, tracking_url, application_id, job_id):
        self._tracking_url = tracking_url
        self._application_id = application_id
        self._job_id = job_id
        threading.Thread.__init__(self)

    def run(self):
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
                                time.sleep(10)
                        except Exception:
                            if "SUCCEEDED" in response.text:
                                # The response is HTML and not JSON, when the job is only in the FINISHED stage.
                                print('SUCCEEDED')
                                break
                            else:
                                traceback.print_exc()
                else:
                    break
