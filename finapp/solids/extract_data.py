from dagster import Field, op, Out, List, get_dagster_logger, Array, Noneable
import datetime
import pandas as pd
import gcsfs
from finapp.schemas.bonds import BondPricesDgType, BondPricesCanadaDgType

logger = get_dagster_logger()


@op(name='get_bond_price',
    config_schema={'isin': Field(str),
                   "from": Field(str), "to": Field(str)},
    required_resource_keys={'finnhub_client'},
    out=Out(io_manager_key="gcs_parquet_io_manager", dagster_type=BondPricesDgType)
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
    del results
    df['isin'] = isin
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'id', 'c': 'close', 's': 'status', 't': 'date'},
              inplace=True)

    df['date'] = pd.to_datetime(df['date'], unit='s')
    df = df.reindex(columns=['id', 'isin', 'close', 'status', 'date'])
    return df


@op(name='get_bond_price_canada',
    config_schema={'path_file': Field(str, default_value='finapp/landing/bond_yields_all_noheader.csv',
                                      is_required=False),
                   "Columns": Field(Noneable(Array(str)))},
    out=Out(dagster_type=BondPricesCanadaDgType)
    )
def get_bond_price_canada(context):
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

    path_file = context.solid_config["path_file"]
    list_columns = context.solid_config["Columns"]
    fs = gcsfs.GCSFileSystem()
    columns_to_extract = ["date"] + ["CDN.AVG.1YTO3Y.AVG", "BD.CDN.2YR.DQ.YLD"]

    logger.info('Extracting data from: ' + path_file)
    with fs.open(path_file) as f:
        data = pd.read_csv(f, names=columns_to_extract, index_col=False, header=1)
    data = data.dropna()
    data["date"] = pd.to_datetime(data['date'])
    new_columns = [col.replace(".", "_") for col in data.columns]
    data.columns = new_columns

    logger.info('Extracted data from: ' + path_file)
    return data
