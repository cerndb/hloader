#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import logging
import os
import threading

from hloader.entities.Job import Job
from itertools import imap

__author__ = 'dstein'

logging.basicConfig()


class ITransferRunner(threading.Thread):
    """
    :type _job: Job
    """

    def __init__(self, job, transfer_instance):
        self._job = job
        self.transfer_instance = transfer_instance
        threading.Thread.__init__(self)

    def run(self):
        # create a Transfer entity for the job
        # prepare the sqoop command
        # start the transfer
        #  monitor the transfer
        pass

    @property
    def sqoop_command(self):
        command = ["sqoop-import"]

        # --------------------------------------------------------------------------------------------------------------
        # COMMON ARGUMENTS
        # --------------------------------------------------------------------------------------------------------------

        # --connect <jdbc-uri>
        #         Specify JDBC connect string
        command.append("--connect")
        command.append(self.generate_connection_string())

        # --connection-manager <class-name>
        #         Specify connection manager class to use

        # --driver <class-name>
        #         Manually specify JDBC driver class to use

        # --hadoop-mapred-home <dir>
        #         Override $HADOOP_MAPRED_HOME

        # --help
        #         Print usage instructions

        # --password-file
        #         Set path for a file containing the authentication password

        # -P
        #         Read password from console
        command.append("-P")

        # --password <password
        #         Set authentication password

        # --username <username>
        #         Set authentication username
        username = os.environ.get("HLOADER_ORACLE_READER_USER", "")
        command.append("--username")
        command.append(username)

        # --verbose
        #         Print more information while working
        command.append("--verbose")

        # --connection-param-file <filename>
        #         Optional properties file that provides connection parameters

        # --relaxed-isolation
        #         Set connection transaction isolation to read uncommitted for the mappers.

        # --------------------------------------------------------------------------------------------------------------
        # VALIDATION ARGUMENTS
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        # IMPORT ARGUMENTS
        # --------------------------------------------------------------------------------------------------------------

        # --append
        #         Append data to an existing dataset in HDFS

        # --as-avrodatafile
        #         Imports data to Avro Data Files

        # --as-sequencefile
        #         Imports data to SequenceFiles

        # --as-textfile
        #         Imports data as plain text (default)

        # --as-parquetfile
        #         Imports data to Parquet Files

        # --boundary-query <statement>
        #         Boundary query to use for creating splits

        # --columns <col,col,col…>
        #         Columns to import from table

        # --delete-target-dir
        #         Delete the import target directory if it exists

        # --direct
        #         Use direct connector if exists for the database
        if (self._job.sqoop_direct):
            command.append("--direct")

        # --fetch-size <n>
        #         Number of entries to read from database at once.

        # --inline-lob-limit <n>
        #         Set the maximum size for an inline LOB

        # -m,--num-mappers <n>
        #         Use n map tasks to import in parallel
        if (self._job.sqoop_nmap):
            command.append("--num-mappers")
            command.append(self._job.sqoop_nmap)

        # -e,--query <statement>
        #         Import the results of statement.
        # TODO use custom built queries instead of tablename

        # --split-by <column-name>
        #         Column of the table used to split work units. Cannot be used with --autoreset-to-one-mapper option.

        # --autoreset-to-one-mapper
        #         Import should use one mapper if a table has no primary key and no split-by column is provided. Cannot be used with --split-by <col> option.

        # --table <table-name>
        #         Table to read
        command.append("--table")
        command.append(self._job.source_table_name)

        # --target-dir <dir>
        #         HDFS destination dir
        command.append("--target-dir")
        # TODO put the right base path here, maybe check the target directory
        command.append(
            "/user/playground/{dbname}/{tablename}/{relative}".format(
                dbname=self._job.source_database_name,
                tablename=self._job.source_table_name,
                relative=self._job.destination_path)
        )

        # --warehouse-dir <dir>
        #         HDFS parent for table destination

        # --where <where clause>
        #         WHERE clause to use during import

        # -z,--compress
        #         Enable compression

        # --compression-codec <c>
        #         Use Hadoop codec (default gzip)

        # --null-string <null-string>
        #         The string to be written for a null value for string columns

        # --null-non-string <null-string>
        #         The string to be written for a null value for non-string columns

        # exit after running the command
        command.append("; exit")

        print command
        command = imap(str, command)

        command_string = " ".join(command)

        logger = logging.getLogger(__name__)
        logger.info(command_string)

        return command_string

    def generate_connection_string(self):
        server = self._job.get_source_server()
        connection_string = "jdbc:oracle:thin:@{address}:{port}/{dbname}".format(address=server.server_address,
                                                                                 port=server.server_port,
                                                                                 dbname=self._job.source_database_name)

        return connection_string
