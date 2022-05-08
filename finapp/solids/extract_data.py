from dagster import solid, Noneable, Field
from quandl import ApiConfig
from decouple import AutoConfig
import quandl
import datetime
import pandas as pd
config = AutoConfig(search_path='FinApp')


@solid(name='consume_api',
       config_schema={'table_name': Field(str),
                      'compnumber': Field(Noneable(str), default_value='39102'),
                      'schema': Field(str)})
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


@solid(name='get_bond_price',
       config_schema={'isin': Field(str),
                      "from": Field(str), "to": Field(str)},
       required_resource_keys={'finnhub_client'}
       )
def get_bond_price(context):
    """
        Api to download bond prices
        Args:
            api_key (str) : path to api key
            ticker (str) : ticker of the stock
            frequency (str) : aggregation time of the stock price
            from (str) :  intial datetime of the stock
            to (str) : final datetime of the stock

        Returns:
            df (Dataframe) : output data
        """

    finnhub_client = context.resources.finnhub_client
    isin = context.solid_config["isin"]
    from_datetime = context.solid_config["from"]
    from_datetime = int(datetime.datetime.timestamp(datetime.datetime.strptime(from_datetime, "%Y-%m-%d")))
    to_datetime = context.solid_config["to"]
    to_datetime = int(datetime.datetime.timestamp(datetime.datetime.strptime(to_datetime, "%Y-%m-%d")))
    results = finnhub_client.bond_price(isin, from_datetime, to_datetime)
    df = pd.DataFrame(results)
    df['isin'] = isin
    df.reset_index(inplace=True)
    df.rename(columns={'c': 'close', 's': 'status', 't': 'date'},
              inplace=True)

    df['date'] = pd.to_datetime(df['date'], unit='s')
    df = df.reindex(columns=['id', 'isin', 'close', 'status', 'date'])
    return df