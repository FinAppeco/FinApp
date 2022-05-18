from dagster import Field, op
from decouple import AutoConfig
import datetime
import pandas as pd

config = AutoConfig(search_path='FinApp')


@op(name='get_bond_price',
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
