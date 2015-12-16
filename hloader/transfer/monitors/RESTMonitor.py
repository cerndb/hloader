import re
import threading
import time
import traceback
import requests



HTML_UPDATE_WAIT_SECONDS = 1
UPDATE_WAIT_SECONDS = 10


class RESTMonitor(threading.Thread):
    """
    REST API monitoring class, to be run on a parallel thread.
    """

    def __init__(self, tracking_url, application_id, job_id):
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
                        time.sleep(HTML_UPDATE_WAIT_SECONDS)
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

                                # TODO what if there is no SUCCEEDED? Load archived log.
                else:
                    break

    def _update_log(self, source):
        """
        Use the @DatabaseManager to update the logs for this transfer.

        :param source: The identifier of the source for this update.
        """
        # TODO Database communication
        pass

    def _update_status(self):
        """
        Use the @DatabaseManager to update the status of this transfer and also update the status history.
        """
        # TODO Database communication
        pass
