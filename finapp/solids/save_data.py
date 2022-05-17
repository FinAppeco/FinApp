from dagster import solid
from dagster_pandas import DataFrame
import os
import pandas as pd
@solid(name="local_save")
def local_save(context, df: DataFrame) -> None:
    """Save the output as excel in local.

    Args:
        df (pd.DataFrame): dataframe to be stored as Excel file
        name_file (str): Name of the file

    Returns:
        pd.DataFrame: data with new fields name
    """
    path_file = os.path.dirname(__file__)
    folder = os.path.abspath(os.path.join(path_file, "..", "data"))
    writer = pd.ExcelWriter(os.path.join(folder, context.pipeline_name+".xlsx"), engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.save()