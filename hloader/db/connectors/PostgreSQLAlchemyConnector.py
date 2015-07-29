from __future__ import absolute_import

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from hloader.db.IDatabaseConnector import IDatabaseConnector
from hloader.db.connectors.sqlaentities.HadoopCluster import HadoopCluster
from hloader.db.connectors.sqlaentities.Job import Job
from hloader.db.connectors.sqlaentities.Log import Log
from hloader.db.connectors.sqlaentities.OracleServer import OracleServer
from hloader.db.connectors.sqlaentities.Transfer import Transfer

import signal
import sys

DEBUG = False

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

    def __init__(self, address, port, username, password, database):
        self._engine = create_engine(
            "postgresql://{username}:{password}@{address}:{port}/{database}".format(
                username=username,
                password=password,
                address=address,
                port=port,
                database=database
            ), echo=DEBUG)

        # Test, whether the connection can be made
        try:
            self._engine.connect().close()
        except Exception:
            # TODO better error handling
            raise

        self.session_factory = sessionmaker(bind=self._engine)


    #
    # REST API data source methods
    # ------------------------------------------------------------------------------------------------------------------

    def create_session(self):
        """
        Returns a scoped session object from the Session Factory.
        PostgreSQLAlchemyConnector should never create any session (scoped, or otherwise) to access the database.
        Instead, the session returned by this method should be supplied to the functions in PostgreSQLAlchemyConnector
        wherever there is a need for a session to access the database.
        :return: sqlalchemy.orm.session.Session
        """

        return scoped_session(self.session_factory)

    def get_servers(self, _session, **kwargs):
        """
        Queries the HL_SERVERS table and returns a list of available Oracle servers based on the keyword arguments
        passed.

        :param kwargs: Zero or more of the following arguments - server_id, server_port, server_name, server_address
        :return: List of @OracleServers
        :
        """
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', 0)

        for key, value in kwargs.items():
            if value is None:
                kwargs.pop(key, None)

        if len(kwargs):
            return _session.query(OracleServer).filter_by(**kwargs).limit(limit).offset(offset).all()
        else:
            return _session.query(OracleServer).limit(limit).offset(offset).all()

    def get_clusters(self, _session, **kwargs):
        """
        Get every available @HadoopCluster that the user could select as the destination cluster.

        :return: Set of available clusters.
        """
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', 0)

        for key, value in kwargs.items():
            if value is None:
                kwargs.pop(key, None)

        if len(kwargs):
            return _session.query(HadoopCluster).filter_by(**kwargs).limit(limit).offset(offset).all()
        else:
            return _session.query(HadoopCluster).limit(limit).offset(offset).all()

    def get_jobs(self, _session, **kwargs):
        """
        Get every @Job stored in the database. If the @serverid is set, only return jobs accessing databases on that
        server. If the @database parameter is also set, only selects jobs accessing that database.

        :param server: The entity or the ID of the accessed source server.
        :param database: Name of the accessed database.

        :type server [OracleServer_ | int]
        :type database: str

        :return: Set of selected jobs.
        """
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', 0)

        for key, value in kwargs.items():
            if value is None:
                kwargs.pop(key, None)

        if len(kwargs):
            return _session.query(Job).filter_by(**kwargs).limit(limit).offset(offset).all()
        else:
            return _session.query(Job).limit(limit).offset(offset).all()

    def get_transfers(self, _session, **kwargs):
        """
        Get every @Transfer that satisfies the constraints. If there are too many transfers, setting @start and @limit
        enables paginating of the results.

        :param job: Job constraint, If set, only select transfers for that job. The parameter could either be a @Job or
        the ID of the job (integer).
        :param state: Stat constraint. If set, only select transfers that are in this state.
        :param start: Paginating constraint. Start offset of the result set.
        :param limit: Paginating constraint. Length of a page of the result set.

        :type job: [Job_ | int]
        :type state: Transfer_.Status
        :type start: int
        :type limit: int

        :return:
        """
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', 0)

        order = kwargs.pop('order', None)

        parameter_map = {
            'transfer_id': "Transfer.transfer_id"
        }

        if order:
            order = getattr(self, parameter_map[order.split('.')[0]] + "." + order.split('.')[1])

        for key, value in kwargs.items():
            if value is None:
                kwargs.pop(key, None)

        if len(kwargs):
            return _session.query(Transfer)\
                .filter_by(**kwargs)\
                .limit(limit)\
                .order_by(order)\
                .offset(offset)\
                .all()
        else:
            return _session.query(Transfer).limit(limit).offset(offset).all()

            # TODO: state handling

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

    def get_log(self, _session, transfer, source):
        """

        :param transfer:
        :param source:

        :type transfer: Transfer
        :type source: str
        :return:
        """

        # TODO: Need to test if we can make do without the line below
        # log = _session.query(Log).filter(Log.transfer == transfer, Log.log_source == source).first()

        log = None
        if not log:
            log = Log()
            log.transfer = transfer
            log.log_source = source
        _session.add(log)
        _session.commit()

        return log

    def save_log(self, _session, log):
        # TODO
        """

        :param log:

        :type log: Log

        :return:
        """
        _session.add(log)
        _session.commit()

    def create_transfer(self, _session, job, transfer_instance_id):
        # TODO
        """

        :param job:

        :type job Job

        :return:
        """
        transfer = Transfer()
        transfer.job = job
        transfer.scheduler_transfer_id = transfer_instance_id
        _session.add(transfer)

        self.modify_status(_session, transfer, Transfer.Status.WAITING)

        _session.commit()
        return transfer

    def modify_status(self, _session, transfer, status):
        # TODO
        """
        :param transfer:
        :param status:

        :type transfer: Transfer
        :type status: str

        :rtype: None
        """
        transfer.transfer_status = status

        # TODO proper status handling
        # Create new history entry

        _session.commit()

    def setup_database(self):
        # TODO
        """

        :return:
        """
        from hloader.db.connectors.sqlaentities.Base import Base

        Base.metadata.create_all(bind=self._engine)
