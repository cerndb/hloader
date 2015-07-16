from __future__ import absolute_import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hloader.db.IDatabaseConnector import IDatabaseConnector
from hloader.db.connectors.sqlaentities.HadoopCluster import HadoopCluster
from hloader.db.connectors.sqlaentities.Job import Job
from hloader.db.connectors.sqlaentities.Log import Log
from hloader.db.connectors.sqlaentities.OracleServer import OracleServer
from hloader.db.connectors.sqlaentities.Transfer import Transfer
from hloader.entities.HadoopCluster import HadoopCluster as HadoopCluster_
from hloader.entities.Job import Job as Job_
from hloader.entities.OracleServer import OracleServer as OracleServer_
from hloader.entities.Transfer import Transfer as Transfer_

DEBUG = True

__author__ = 'dstein'


class PostgreSQLAlchemyConnector(IDatabaseConnector):
    """
    Interface that has to be implemented by every Database Connector transferred by the @DatabaseManager.
    It contains every method stub used by the REST API provider and other Hadoop-connected parts of the software, eg.,
    @SSHRunner.

    Apart from the basic CRUD operations, it should be able to retrieve entities satisfying more complex constraints.

    :type _engine: Engine
    :type _session: sqlalchemy.orm.session.Session
    """

    Session = sessionmaker()

    def __init__(self, address, port, username, password, database):
        self._engine = create_engine(
            "postgresql://{username}:{password}@{address}:{port}/{database}".format(
                username=username,
                password=password,
                address=address,
                port=port,
                database=database
            ), echo=True)

        # Test, whether the connection can be made
        try:
            self._engine.connect().close()
        except Exception:
            # TODO better error handling
            raise

        PostgreSQLAlchemyConnector.Session.configure(bind=self._engine)
        self._session = PostgreSQLAlchemyConnector.Session()

    #
    # REST API data source methods
    # ------------------------------------------------------------------------------------------------------------------

    def get_servers(self):
        """
        Get every available @OracleServer that the user could select as a source server.
        :return: Set of available servers.
        """
        return self._session.query(OracleServer).all()

    def get_clusters(self):
        """
        Get every available @HadoopCluster that the user could select as the destination cluster.
        :return: Set of available clusters.
        """
        return self._session.query(HadoopCluster).all()

    def get_jobs(self, server=None, database=None):
        """
        Get every @Job stored in the database. If the @serverid is set, only return jobs accessing databases on that
        server. If the @database parameter is also set, only selects jobs accessing that database.
        :param server: The entity or the ID of the accessed source server.
        :param database: Name of the accessed database.
        :return: Set of selected jobs.
        """
        query = self._session.query(Job)

        if server:
            if server.isinstance(OracleServer):
                query = query.filter(Job.source_server == server)
            elif server.isinstance(int):
                query = query.filter(Job.source_server_id == server)

        if database:
            query = query.filter(Job.source_database_name == database)

        return query.all()

    def get_transfers(self, job=None, state=None, start=None, limit=None):
        """
        Get every @Transfer that satisfies the constraints. If there are too many transfers, setting @start and @limit
        enables paginating of the results.

        :type job: [Job_ | int]

        :param job: Job constraint, If set, only select transfers for that job. The parameter could either be a @Job or
        the ID of the job (integer).
        :param state: Stat constraint. If set, only select transfers that are in this state.
        :param start: Paginating constraint. Start offset of the result set.
        :param limit: Paginating constraint. Length of a page of the result set.
        :return:
        """
        query = self._session.query(Transfer)

        if job:
            if job.isinstance(Job_):
                query = query.filter(Transfer.job == job)
            elif job.isinstance(int):
                query = query.filter(Transfer.job_id == job)

        # TODO state handling
        # if state

        if start and limit:
            query = query.slice(start, start + limit)

        return query.all()

    #
    # Inner methods
    # ------------------------------------------------------------------------------------------------------------------

    # def get_ready_jobs(self):
    #     """
    #     Get every @Job that is ready and enabled to be run. A job is only enabled, if its last transfer was successful
    #     (if any), and the time difference since is greater than the user-provided value. Also, it is not not actually
    #     running.
    #     :return: Set of jobs ready to start.
    #     """
    #     last_transfer = self._session.query(
    #         Transfer.job_id,
    #         func.max(Transfer.transfer_start).label("last_transfer")
    #     ).group_by(Transfer.job_id).subquery()
    #
    #     last_transfer_data = self._session.query(Transfer) \
    #         .join(last_transfer, Transfer.job_id == last_transfer.c.job_id) \
    #         .filter(Transfer.transfer_last_update == last_transfer.c.last_transfer).subquery()
    #
    #     jobs_last_transfer = self._session.query(Job, last_transfer_data).outerjoin(last_transfer_data) \
    #         .filter(
    #         or_(
    #             and_(
    #                 last_transfer_data.c.transfer_id == None,
    #                 Job.start_time < func.now()
    #             ),
    #             and_(
    #                 last_transfer_data.c.transfer_start < func.floor(
    #                     func.cast((func.now() - last_transfer_data.c.transfer_start), Integer)
    #                     / Job.interval) * Job.interval + Job.start_time,
    #                 and_(
    #                     last_transfer_data.c.transfer_status != "RUNNING",
    #                     last_transfer_data.c.transfer_status != "FAILED"
    #                 )
    #             )
    #         )).all()
    #
    #     return self._session.query(Job).filter(or_(Job.transfers))

    def get_log(self, transfer, source):
        log = self._session.query(Log).filter(Log.transfer == transfer).filter(Log.log_source == source).first()
        if not log:
            log = Log()
            log.transfer = transfer
            log.log_source = source

        return log

    def save_log(self, log):
        self._session.add(log)
        self._session.commit()

    def create_transfer(self, job):
        transfer = Transfer()
        transfer.job = job
        self._session.add(transfer)

        self.modify_status(transfer, "PENDING")

        self._session.commit()
        return transfer

    def modify_status(self, transfer, status):

        transfer.transfer_status = status

        # TODO proper status handling
        # Create new history entry

        self._session.commit()

    def setup_database(self):
        from hloader.db.connectors.sqlaentities.Base import Base
        Base.metadata.create_all(bind=self._engine)