import pandera as pa
from dagster_pandera import pandera_schema_to_dagster_type
from pandera.typing import Series, String, Float, Int

import pandas as pd


class BondPrices(pa.SchemaModel):
    """Open/high/low/close prices for a set of stocks by day."""
    id: Series[Int] = pa.Field(ge=0, description='Id ')
    isin: Series[String] = pa.Field(description="Code of the bond")
    close: Series[Float] = pa.Field(ge=0, description="open prices")
    status: Series[String] = pa.Field(description="Status of the response. This field can either be ok or no_data.")
    date: Series[pd.Timestamp] = pa.Field(description="Date of prices")


BondPricesDgType = pandera_schema_to_dagster_type(BondPrices)