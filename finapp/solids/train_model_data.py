import pandas as pd
from dagster import op
from dagster_mlflow import end_mlflow_on_run_finished, mlflow_tracking


@op(name='cleaning_and_transformation_bonds')
def bond_model_training(context, df):
    #TODO: shikur has to put here the cleaning and transform steps and this must to return a dataframa
    mlflow.log_params(some_params)
    mlflow.tracking.MlflowClient().create_registered_model(some_model_name)