import requests
import requests_mock

from hloader.db.DatabaseManager import DatabaseManager

class OozieRunner(object):
    
    def submit(self, job):
        server=DatabaseManager.meta_connector.get_source_server_for_job(job) 
        cluster=DatabaseManager.meta_connector.get_destination_cluster_for_job(job)

        #TODO authentication
        sqoop_command = "import --append --connect jdbc:oracle:thin:@(description=(address=(protocol=tcp)(host={host})(port={port}))(connect_data=(service_name={service}))) --username X --password X --table {schema}.{table} --target-dir {directory} -m 1".format(host=server.server_address,
             port=server.server_port,
             service=server.server_service,
             schema=job.source_schema_name,
             table=job.source_object_name,
             directory=job.destination_path)

        config_xml = """<?xml version="1.0" encoding="UTF-8"?>
                          <configuration>
                              <property>
                                  <name>user.name</name>
                                  <value>{username}</value>
                              </property>
                              <property>
                                  <name>nameNode</name>
                                  <value>hdfs://localhost:8020</value>
                              </property>
                              <property>
                                  <name>jobTracker</name>
                                  <value>localhost:8032</value>
                              </property>
                              <property>
                                  <name>sqoopCommand</name>
                                  <value>{sqoop_command}</value>
                              </property>
                              <property>
                                  <name>oozie.use.system.libpath</name>
                                  <value>True</value>
                              </property>""".format(username=job.owner_username,
                                             sqoop_command=sqoop_command)
                       
        
        # check whether workflow or coordinator
        if(job.coordinator_suffix is not None):
            config_xml+="""<property>
                               <name>oozie.coord.application.path</name>
                               <value>hdfs://localhost:8020/user/{username}/{coordinator}/</value>
                           </property>
                           <property>
                               <name>wf_application_path</name>
                               <value>hdfs://localhost:8020/user/{username}/{workflow}</value>
                           </property>
                           <property>
                               <name>start_date</name>
                               <value>{start_date}</value>
                           </property>
                           <property>
                               <name>end_date</name>
                               <value>{end_date}</value>
                           </property>
                           <property>
                               <name>freq</name>
                               <value>{freq}</value>
                           </property>""".format(username=job.owner_username,
                                                 coordinator=job.coordinator_suffix,
                                                 workflow=job.workflow_suffix,
                                                 start_date=job.start_time[:16]+'Z',
                                                 end_date=job.end_time[:16]+'Z',
                                                 freq=job.interval)
 
        else:
            config_xml+="""<property>
                               <name>oozie.wf.application.path</name>
                               <value>hdfs://localhost:8020/user/{username}/{workflow}/</value>
                           </property>""".format(username=job.owner_username,
                                                 workflow=job.workflow_suffix)

        config_xml+="</configuration>"

        session = requests.Session()
        #for unit testing
        adapter = requests_mock.Adapter()
        session.mount('mock', adapter)
        adapter.register_uri('POST', 'mock://test.com/v2/jobs', text='data')

        headers = {'Content-Type': 'application/xml', 'charset': 'UTF-8'}
        response = session.post(cluster.oozie_url+'v2/jobs',
                                data=config_xml, headers=headers)

        if response.status_code == 201:
            return response.json()['id']

    def manage(self, job, action):
        """

        :param job:
        :param action:
        :return:
        """
        if action not in ('start', 'suspend', 'resume', 'kill', 'dryrun'):
            print("Unsupported action")
        
        cluster=DatabaseManager.meta_connector.get_destination_cluster_for_job(job)

        URL = cluster.oozie_url+'v2/job/{job}?action={action}'.format(job=job.oozie_job_id, action=action)

        session = requests.Session()
        #for unit testing
        adapter = requests_mock.Adapter()
        session.mount('mock', adapter)
        adapter.register_uri('PUT', 'mock://test.com/v2/job/None?action=start', text='data')

        response = session.put(URL)
        return response.status_code

    def job_info(self, job, timezone = "CET"):
        """

        :param job:
        :param timezone:
        :return:
        """
        cluster=DatabaseManager.meta_connector.get_destination_cluster_for_job(job)

        URL = cluster.oozie_url+'v2/job/{job}?show=info&timezone={timezone}'.format(job=job.oozie_job_id, timezone=timezone)

        response = requests.post(URL)
        if response.status_code == 200:
            return response.json()
