import pandera as pa
from dagster_pandera import pandera_schema_to_dagster_type
from pandera.typing import Series, String, Float, Int

import pandas as pd

class CABondPrices(pa.SchemaModel):
    """Open/high/low/close prices for a set of stocks by day."""
    Date: Series[pd.Timestamp] = pa.Field(description="Date of prices")
    V39062: Series[String] = pa.Field(description="Code of the bond")
    V39056: Series[Float] = pa.Field(ge=0, description="open prices")
    V39057: Series[String] = pa.Field(description="Status of the response. This field can either be ok or no_data.")


CABondPricesDgType = pandera_schema_to_dagster_type(CABondPrices)