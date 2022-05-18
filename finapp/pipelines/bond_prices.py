from dagster import graph, job

from finapp.resources.custom_clients import finnhub_client
from finapp.resources.get_config_jobs import PipelineConfiguration
from finapp.solids.extract_data import get_bond_price

# Mode definitions allow you to configure the behavior of your pipelines and solids at execution
# time. For hints on creating modes in Dagster, see our documentation overview on Modes and
# Resources: https://docs.dagster.io/overview/modes-resources-presets/modes-resources
from finapp.solids.save_data import local_save

test_config = PipelineConfiguration(name='bond_price_prediction_api', resource={'finnhub_client': finnhub_client})

@graph()
def get_bond_prices():
    """
    A graph definition to predict bond price
    """
    df = get_bond_price()
    local_save(df)


config_bonds = test_config.get_preset(name_yaml='bond_price.yaml')
@job(name='get_bond_prices_api',
     resource_defs=test_config.get_io_managers(),
     description="Pipeline for bond prices",
     config=config_bonds)
def get_bond_prices_api():
    return get_bond_prices()

