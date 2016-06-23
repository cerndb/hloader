DROP TABLE IF EXISTS hl_clusters CASCADE;

CREATE TABLE hl_clusters
  (
    cluster_id      SERIAL NOT NULL ,
    cluster_address TEXT NOT NULL ,
    cluster_name    TEXT NOT NULL
  ) ;
ALTER TABLE hl_clusters ADD CONSTRAINT hl_clusters_pk PRIMARY KEY ( cluster_id ) ;

DROP TABLE IF EXISTS hl_jobs CASCADE;
CREATE TABLE hl_jobs
  (
    job_id                   SERIAL NOT NULL ,
    source_server_id         INTEGER NOT NULL ,
    source_schema_name       TEXT NOT NULL ,
    source_object_name       TEXT NOT NULL ,
    destination_cluster_id   INTEGER NOT NULL ,
    destination_path         TEXT NOT NULL ,
    owner_username           TEXT NOT NULL ,
    sqoop_nmap               INTEGER ,
    sqoop_splitting_column   TEXT ,
    sqoop_incremental_method TEXT ,
    sqoop_direct             INTEGER NOT NULL ,
    start_time               TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP ,
    interval                 INTERVAL ,
    job_last_update          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  ) ;
COMMENT ON COLUMN hl_jobs.update_difference
IS
  'The minimal difference (in hours) between the start of the actual day and the next timestamp the job is ready to be scheduled.' ;
  ALTER TABLE hl_jobs ADD CONSTRAINT hl_jobs_pk PRIMARY KEY ( job_id ) ;

DROP TABLE IF EXISTS hl_logs CASCADE;
CREATE TABLE hl_logs
  (
    log_id      SERIAL NOT NULL ,
    transfer_id INTEGER NOT NULL ,
    log_source  TEXT NOT NULL ,
    log_path    TEXT,
    log_content TEXT
  ) ;
ALTER TABLE hl_logs ADD CONSTRAINT hl_logs_pk PRIMARY KEY ( log_id ) ;

DROP TABLE IF EXISTS hl_servers CASCADE;
CREATE TABLE hl_servers
  (
    server_id      SERIAL NOT NULL ,
    server_address TEXT NOT NULL ,
    server_port    INTEGER NOT NULL ,
    server_name    TEXT NOT NULL
  ) ;
ALTER TABLE hl_servers ADD CONSTRAINT hl_oracle_servers_pk PRIMARY KEY ( server_id ) ;

DROP TABLE IF EXISTS hl_transfers CASCADE;
CREATE TABLE hl_transfers
  (
    transfer_id           SERIAL NOT NULL ,
    scheduler_transfer_id TEXT ,
    job_id                INTEGER NOT NULL ,
    transfer_status       TEXT ,
    transfer_start        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP ,
    transfer_last_update  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP ,
    last_modified_value   TEXT NOT NULL
  ) ;
ALTER TABLE hl_transfers ADD CONSTRAINT hl_transfers_pk PRIMARY KEY ( transfer_id ) ;

ALTER TABLE hl_jobs ADD CONSTRAINT hl_jobs_hl_clusters_fk FOREIGN KEY ( destination_cluster_id ) REFERENCES hl_clusters ( cluster_id ) ON
DELETE CASCADE ;

ALTER TABLE hl_jobs ADD CONSTRAINT hl_jobs_hl_servers_fk FOREIGN KEY ( source_server_id ) REFERENCES hl_servers ( server_id ) ON
DELETE CASCADE ;

ALTER TABLE hl_logs ADD CONSTRAINT hl_logs_hl_transfers_fk FOREIGN KEY ( transfer_id ) REFERENCES hl_transfers ( transfer_id ) ;

ALTER TABLE HL_TRANSFERS ADD CONSTRAINT HL_TRANSFERS_HL_JOBS_FK FOREIGN KEY ( job_id ) REFERENCES HL_JOBS ( job_id ) ;


