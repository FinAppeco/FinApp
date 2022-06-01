import pandas as pd
from dagster import op


@op(name='cleaning_and_transformation_bonds')
def cleaning_and_transformation_bonds(context, df):
    #TODO: shikur has to put here the cleaning and transform steps and this must to return a dataframe
    return pd.DataFrame([])