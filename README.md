[![Build Status](https://travis-ci.org/cerndb/hloader.svg?branch=master)](https://travis-ci.org/cerndb/hloader)

# CERN HLoader
HLoader is a tool built around Apache Sqoop and Oozie for data ingestion from relational databases into Hadoop

# Installation & Configuration

1. Clone the repository (git clone https://github.com/cerndb/hloader.git) 
2. Install the requirements (*pip install -r requirements.txt*) and Oracle .rpm files located in /travis-resources
3. Set up the config.ini (properties starting with *AUTH_* represent the authentication database, while properties starting with *POSTGRE_* represent the meta database)
4. Run HLoader.py

In case you would like to set up the meta database yourself, the script is located in /hloader/db/PostgreSQL_backend_schema.sql

# REST API

The REST API exposes meta data to the user and enables the submission of new ingestion jobs <br>
It runs on http://127.0.0.1:5000 <br>

### The available methods are:

GET /headers<br>
returns PYTHON ENVIRONMENT VARIABLES and REQUEST HEADERS

GET /api/v1<br>
the index page

GET /api/v1/clusters<br>
returns a json with an array of clusters, potentially filtered by an attribute value

GET /api/v1/servers<br>
returns a json with an array of servers, potentially filtered by an attribute value

GET /api/v1/schemas<br>
returns json with arrays of available and unavailable schemas given an owner username. Reuired parameter: *owner_username*

GET /api/v1/jobs<br>
returns a json with an array of jobs, potentially filtered by an attribute value

POST /api/v1/jobs<br>
submits a job and returns a json containing its ID. <br>
Required parameters: *source_server_id, source_schema_name, source_object_name, destination_cluster_id, destination_path, owner_username, workflow_suffix, sqoop_direct* <br>
Optional parameters: *coordinator_suffix, sqoop_nmap, sqoop_splitting_column, sqoop_incremental_method, start_time, end_time, interval, job_last_update*

DELETE /api/v1/jobs<br>
deletes a job given its ID and reports the status of the operation. Required parameter: *job_id*

GET /api/v1/logs<br>
returns a json with an array of logs, potentially filtered by an attribute value

GET /api/v1/transfers<br>
returns a json with an array of transfers, potentially filtered by an attribute value

### A word on Apache Oozie

Currently the submitted jobs will be executed using Oozie Workflows or Coordinators. The path to the Workflow/Coordinator app on HDFS should be provided in the *workflow_suffix / coordinator_suffix* parameters respectively. The URL to the Oozie deployment is contained in the *clusters* meta data.

Sample insert statements for meta data can be found in /hloader/db/PostgreSQL_test_data.sql
