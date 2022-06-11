
from dagster import job , op, Out
#from dagster_pandas import create_dagster_pandas_dataframe_type , PandasColumn
import pandas as pd
from finapp.schemas.caBondPrice import CABondPricesDgType


test_config = PipelineConfiguration(name='get_cabond_prices_api')


TripDataFrame = create_dagster_pandas_dataframe_type(
    name="TripDataFrame",
    columns=[
        PandasColumn.string_column("Date"),
        PandasColumn.string_column("V39062"),
        PandasColumn.string_column("V39056"),
        PandasColumn.string_column("V39057")])

@op(out=Out(TripDataFrame))
def load_trip_dataframe(path) -> pd.DataFrame:
    df = pd.DataFrame()
    #df = pd.read_csv("finapp/local_data/lookup3.csv", on_bad_lines='skip')
    df = pd.read_csv(path, on_bad_lines='skip')

    return df


@op(name='get_cabond_price',
    config_schema={'Date': Field(str),
                   "country": Field(str), "sourceloc": Field(str), "transformloc": Field(str)},

    out=Out(io_manager_key="gcs_parquet_io_manager", dagster_type=CABondPricesDgType)
    )
def get_cabond_price(context):
    shikur= context.solid_config["country"]
    print(shikur)
    df = pd.DataFrame()

    return df



@op
def provideAuth():
    datac = get_us_bond_price("testtoken", "applicationapy")
    print(datac)

"""
@job(name='get_bond_canada_prices_api',
     resource_defs=test_config.get_io_managers(),
     description="Pipeline for bond prices",
     config=config_bonds)
def firsthand_data_ingestion():
    df = get_canada_bond_price()
    print(TripDataFrame)
"""
config_bonds = test_caconfig.get_preset(name_yaml='bond_price.yaml')
@job(name='get_cabond_prices_api',
     resource_defs=test_config.get_io_managers(),
     description="Pipeline for bond prices",
     config=config_bonds)
def get_cabond_prices_api(context):
    get_cabond_price()
    print("shikur")
#if __name__ == "__main__":
 #   print("shikur Begin")
  #  result = firsthand_data_ingestion().execute_in_process()
   # print("shikur end")

