from dagster import solid, Noneable, Field
from quandl import ApiConfig
from decouple import AutoConfig
import quandl
import pandas as pd
config = AutoConfig(search_path='FinApp')


@solid(name='consume_api',
       config_schema={'table_name': Field(str),
                      'compnumber': Field(Noneable(str), default_value='39102'),
                      'schema': Field(str)},
       required_resource_keys={'postgresconnector'})
def consume_api(context):
    """
    A solid definition. This example solid outputs a single string.

    For more hints about writing Dagster solids, see our documentation overview on Solids:
    https://docs.dagster.io/overview/solids-pipelines/solids
    """
    connector = context.resources.postgresconnector
    engine = connector.get_engine()
    ApiConfig.api_key = config('NASDAQ')
    #getting parameters
    compnumber = context.solid_config['compnumber']
    table_name = context.solid_config['table_name']
    schema = context.solid_config['schema']
    #consume data
    data = quandl.get_table('MER/F1', compnumber=compnumber, paginate=True)
    data = pd.DataFrame(data)
    data.to_sql(name=table_name, con=engine, schema=schema, if_exists='replace')
    return "Hello, Dagster!"
