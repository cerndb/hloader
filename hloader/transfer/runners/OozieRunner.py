from __future__ import absolute_import
from hloader.entities.oozie.Job import OozieJob

class OozieRunner(OozieJob):
    def submit(self):
        sqoop_command = ""

        workflow_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>fs.default.name</name>
        <value>{namenode}</value>
    </property>
    <property>
        <name>mapred.job.tracker</name>
        <value>{job_tracker}</value>
    </property>
    <property>
        <name>user.name</name>
        <value>{user}</value>
    </property>
    <property>
        <name>oozie.sqoop.command</name>
        <value>
            {sqoop_command}
        </value>
    </property>
        <name>oozie.libpath</name>
        <value>{oozie_libpath}</value>
    </property>
    <property>
        <name>oozie.proxysubmission</name>
        <value>{oozie_proxy_submission}</value>
    </property>
</configuration>""".format(namenode=self.namenode,
                           job_tracker=self.job_tracker,
                           user=self.user,
                           sqoop_command=sqoop_command,
                           oozie_libpath=self.oozie_libpath,
                           oozie_proxy_submission=self.oozie_proxy_submission)

        headers = {'Content-Type': 'application/xml; charset=utf-8'}
        response = requests.post(urlparse.urljoin(self.oozie_base_URL, '/oozie/v2/jobs?jobtype=sqoop'),
                                 data=workflow_xml, headers=headers)
        if response.status_code == 200:
            return response.json()['id']

    def manage(self, job, action):
        if action not in ('start', 'suspend', 'resume', 'kill', 'dryrun'):
            print "Unsupported action"

        URL = urlparse.urljoin(self.oozie_base_URL,
                                   '/oozie/v2/jobs/{job}?action={action}'
                                   .format(job=job.job_id, action=action)
                                   )
        response = requests.post(URL)
        return response.status_code

    def job_info(self, job, timezone = "CET"):
        URL = urlparse.urljoin(self.oozie_base_URL,
                                   '/oozie/v2/job/{job}?show=info'
                                   '&timezone={timezone}'
                                   .format(job=job.job_id, timezone=timezone)
                                   )

        response = requests.post(URL)
        if response.status_code == 200:
            return response.json()
