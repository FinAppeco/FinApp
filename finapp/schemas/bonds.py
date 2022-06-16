import pandera as pa
from dagster_pandera import pandera_schema_to_dagster_type
from pandera.typing import Series, String, Float, Int, DateTime

import pandas as pd


class BondPrices(pa.SchemaModel):
    """Open/high/low/close prices for a set of stocks by day."""
    id: Series[Int] = pa.Field(ge=0, description='Id ')
    isin: Series[String] = pa.Field(description="Code of the bond")
    close: Series[Float] = pa.Field(ge=0, description="open prices")
    status: Series[String] = pa.Field(description="Status of the response. This field can either be ok or no_data.")
    date: Series[pd.Timestamp] = pa.Field(description="Date of prices")


class BondPricesCanada(pa.SchemaModel):
    """Open/high/low/close prices for a set of stocks by day."""
    date: Series[DateTime] = pa.Field(description="timestamp for the bond")
    CDN_AVG_1YTO3Y_AVG: Series[Float] = pa.Field(ge=0,
                                                 description="1 to 3 year, Government of Canada marketable bonds - Average yield")
    BD_CDN_2YR_DQ_YLD: Series[Float] = pa.Field(ge=0, description="2 year, Government of Canada benchmark bond yields")


BondPricesDgType = pandera_schema_to_dagster_type(BondPrices)
BondPricesCanadaDgType = pandera_schema_to_dagster_type(BondPricesCanada)
