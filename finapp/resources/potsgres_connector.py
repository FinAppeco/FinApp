from sqlalchemy import create_engine
from decouple import config
from dagster import resource, Field


class PostgresConnector(object):

    def __init__( self, schema ):
        self.dbname = config('DBNAME')
        self.user = config('DBUSER')
        self.password = config('DBPASSWORD')
        self.host = config('LOCALHOST')
        self.engine = create_engine('postgresql+psycopg2://{user}:{password}@{hostname}/{database_name}'.format(
            user=self.user,
            password=self.password,
            hostname=self.host,
            database_name=self.dbname,

        ),
        connect_args={'options': '-csearch_path={}'.format(schema)})

    def get_engine( self ):
        return self.engine


@resource(config_schema={'schema': Field(str)})
def get_postgresconnector(context):
    schema = context.resource_config['schema']
    return PostgresConnector(schema=schema)
