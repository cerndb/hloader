DROP TABLE IF EXISTS HL_CLUSTERS CASCADE;

CREATE TABLE HL_CLUSTERS
  (
    cluster_id      SERIAL NOT NULL,
    cluster_address TEXT NOT NULL ,
    cluster_name    TEXT NOT NULL
  ) ;
ALTER TABLE HL_CLUSTERS ADD CONSTRAINT HL_CLUSTERS_PK PRIMARY KEY ( cluster_id ) ;

DROP TABLE IF EXISTS HL_JOBS CASCADE;
CREATE TABLE HL_JOBS
  (
    job_id                   SERIAL NOT NULL,
    source_server_id         INTEGER NOT NULL ,
    source_database_name     TEXT NOT NULL ,
    source_table_name        TEXT NOT NULL ,
    destination_cluster_id   INTEGER NOT NULL ,
    destination_path         TEXT NOT NULL ,
    query_columns            TEXT NOT NULL ,
    query_source             TEXT NOT NULL ,
    query_conditions         TEXT NOT NULL ,
    sqoop_nmap               INTEGER ,
    sqoop_splitting_column   TEXT ,
    sqoop_incremental_method TEXT ,
    sqoop_direct             INTEGER NOT NULL ,
    update_difference        INTEGER
  ) ;
COMMENT ON COLUMN HL_JOBS.update_difference
IS
  'The minimal difference (in hours) between the start of the actual day and the next timestamp the job is ready to be scheduled.' ;
  ALTER TABLE HL_JOBS ADD CONSTRAINT HL_JOBS_PK PRIMARY KEY ( job_id ) ;

DROP TABLE IF EXISTS HL_LOGS CASCADE;
CREATE TABLE HL_LOGS
  (
    log_id      SERIAL NOT NULL,
    transfer_id INTEGER NOT NULL ,
    log_source  TEXT NOT NULL
  ) ;
ALTER TABLE HL_LOGS ADD CONSTRAINT HL_LOGS_PK PRIMARY KEY ( log_id ) ;

DROP TABLE IF EXISTS HL_SERVERS CASCADE;
CREATE TABLE HL_SERVERS
  (
    server_id      SERIAL NOT NULL,
    server_address TEXT NOT NULL ,
    server_port    INTEGER NOT NULL ,
    server_name    TEXT NOT NULL
  ) ;
ALTER TABLE HL_SERVERS ADD CONSTRAINT HL_ORACLE_SERVERS_PK PRIMARY KEY ( server_id ) ;

DROP TABLE IF EXISTS HL_STATUS_HISTORY CASCADE;
CREATE TABLE HL_STATUS_HISTORY
  (
    status_id        SERIAL NOT NULL,
    transfer_id      INTEGER NOT NULL ,
    status_text      TEXT NOT NULL ,
    status_timestamp TIMESTAMP WITH TIME ZONE
  ) ;
ALTER TABLE HL_STATUS_HISTORY ADD CONSTRAINT HL_STATUS_HISTORY_PK PRIMARY KEY ( status_id ) ;


DROP TABLE IF EXISTS HL_TRANSFERS CASCADE;
CREATE TABLE HL_TRANSFERS
  (
    transfer_id          SERIAL NOT NULL,
    job_id               INTEGER NOT NULL ,
    transfer_status      TEXT ,
    transfer_start       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP ,
    transfer_last_update TIMESTAMP WITH TIME ZONE
  ) ;
ALTER TABLE HL_TRANSFERS ADD CONSTRAINT HL_TRANSFERS_PK PRIMARY KEY ( transfer_id ) ;

ALTER TABLE HL_JOBS ADD CONSTRAINT HL_JOBS_HL_CLUSTERS_FK FOREIGN KEY ( destination_cluster_id ) REFERENCES HL_CLUSTERS ( cluster_id ) ON
DELETE CASCADE ;

ALTER TABLE HL_JOBS ADD CONSTRAINT HL_JOBS_HL_SERVERS_FK FOREIGN KEY ( source_server_id ) REFERENCES HL_SERVERS ( server_id ) ON
DELETE CASCADE ;

ALTER TABLE HL_LOGS ADD CONSTRAINT HL_LOGS_HL_TRANSFERS_FK FOREIGN KEY ( transfer_id ) REFERENCES HL_TRANSFERS ( transfer_id ) ;

ALTER TABLE HL_STATUS_HISTORY ADD CONSTRAINT HL_STATUS_HISTORY_HL_TRANSFERS_FK FOREIGN KEY ( transfer_id ) REFERENCES HL_TRANSFERS ( transfer_id ) ;

ALTER TABLE HL_TRANSFERS ADD CONSTRAINT HL_TRANSFERS_HL_JOBS_FK FOREIGN KEY ( job_id ) REFERENCES HL_JOBS ( job_id ) ;


