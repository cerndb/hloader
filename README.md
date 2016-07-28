[![Build Status](https://travis-ci.org/cerndb/hloader.svg?branch=master)](https://travis-ci.org/cerndb/hloader)

CERN HLoader

To launch HLoader:

1. Install the requirements (*pip install -r requirements.txt*)
2. Set up the config.ini (properties starting with *AUTH_* represent the authentication database, while properties starting with *POSTGRE_* represent the meta database)
3. Run HLoader.py

REST API runs on http://127.0.0.1:5000

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
