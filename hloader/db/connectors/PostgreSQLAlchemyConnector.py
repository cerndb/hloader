from sqlalchemy import create_engine
from hloader.entities.HadoopCluster import HadoopCluster
from hloader.entities.Job import Job
from hloader.entities.OracleServer import OracleServer
from hloader.entities.Transfer import Transfer

__author__ = 'dstein'


class PostgreSQLAlchemyConnector:

    engine = create_engine("postgresql://hloader:***@dbod-itdbp1.cern.ch:6600/hloader")

    """
    Interface that has to be implemented by every Database Connector transferred by the @DatabaseManager.
    It contains every method stub used by the REST API provider and other Hadoop-connected parts of the software, eg.,
    @SSHRunner.

    Apart from the basic CRUD operations, it should be able to retrieve entities satisfying more complex constraints.
    """

    #
    # REST API data source methods
    # ------------------------------------------------------------------------------------------------------------------

    def get_servers(self) -> set(OracleServer):
        """
        Get every available @OracleServer that the user could select as a source server.
        :return: Set of available servers.
        """
        raise Exception("Not implemented.")

    def get_clusters(self) -> set(HadoopCluster):
        """
        Get every available @HadoopCluster that the user could select as the destination cluster.
        :return: Set of available clusters.
        """
        raise Exception("Not implemented.")

    def get_jobs(self,
                 serverid: [OracleServer | int]=None,
                 database: str=None
                 ) -> set(Job):
        """
        Get every @Job stored in the database. If the @serverid is set, only return jobs accessing databases on that
        server. If the @database parameter is also set, only selects jobs accessing that database.
        :param serverid: The entity or the ID of the accessed source server.
        :param database: Name of the accessed database.
        :return: Set of selected jobs.
        """
        raise Exception("Not implemented.")

    def get_ready_jobs(self) -> set(Job):
        """
        Get every @Job that is ready and enabled to be run. A job is only enabled, if its last transfer was successful
        (if any), and the time difference since is greater than the user-provided value. Also, it is not not actually
        running.
        :return: Set of jobs ready to start.
        """
        raise Exception("Not implemented.")

    def get_transfers(self,
                      job: [Job | int]=None,
                      state: Transfer.Status=None,
                      start: int=None,
                      limit: int=None
                      ) -> set(Transfer):
        """
        Get every @Transfer that satisfies the constraints. If there are too many transfers, setting @start and @limit
        enables paginating of the results.

        :type job: [Job | int]

        :param job: Job constraint, If set, only select transfers for that job. The parameter could either be a @Job or
        the ID of the job (integer).
        :param state: Stat constraint. If set, only select transfers that are in this state.
        :param start: Paginating constraint. Start offset of the result set.
        :param limit: Paginating constraint. Length of a page of the result set.
        :return:
        """
        raise Exception("Not implemented.")

    #
    # Inner methods
    # ------------------------------------------------------------------------------------------------------------------

    
