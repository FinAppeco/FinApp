from dagster import ModeDefinition, pipeline, PresetDefinition
import os
from finapp.resources.custom_clients import finnhub_client
from finapp.solids.extract_data import get_bond_price
from pathlib import Path
# Mode definitions allow you to configure the behavior of your pipelines and solids at execution
# time. For hints on creating modes in Dagster, see our documentation overview on Modes and
# Resources: https://docs.dagster.io/overview/modes-resources-presets/modes-resources
from finapp.solids.save_data import local_save

path = os.path.join(Path(__file__).parent, 'config_pipelines', 'bond_price.yaml')
MODE = ModeDefinition(name="dev",
                      resource_defs={'finnhub_client' : finnhub_client},
                      )
PRESET = PresetDefinition.from_files(name='bond_price',
                                     config_files=[path],
                                     mode='dev'
                          )


@pipeline(mode_defs=[MODE], preset_defs=[PRESET])
def bond_prices_pipeline():
    """
    A pipeline definition. This example pipeline has a single solid.

    For more hints on writing Dagster pipelines, see our documentation overview on Pipelines:
    https://docs.dagster.io/overview/solids-pipelines/pipelines
    """
    df = get_bond_price()
    local_save(df)