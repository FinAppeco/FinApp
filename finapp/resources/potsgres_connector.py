from sqlalchemy import create_engine
from decouple import config
from dagster import resource, Field


class PostgresConnector(object):

    def __init__( self, schema ):
        self.user = config("DAGSTER_PG_USERNAME")
        self.host = config("DAGSTER_PG_OP_DB")
        self.database = config("DAGSTER_PG_OP_DB")
        self.port = config("DAGSTER_PG_OP_DB_PORT")
        options = "-c search_path=temp"
        connstr = "postgresql://{user}@{host}:{port}/{database}".format(user=self.user,
                                                                        host=self.host,
                                                                        database=self.database,
                                                                        port=self.port
                                                                        )
        self._engine = create_engine(connstr,
                                     connect_args={'password': config('DAGSTER_PG_PASSWORD'),
                                                   'options': options},
                                     isolation_level="REPEATABLE READ")

    def get_engine( self ):
        return self.engine


@resource(config_schema={'schema': Field(str)})
def get_postgresconnector(context):
    schema = context.resource_config['schema']
    return PostgresConnector(schema=schema)
