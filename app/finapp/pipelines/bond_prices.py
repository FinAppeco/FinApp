from dagster import ModeDefinition, pipeline, PresetDefinition, file_relative_path
import os
from app.finapp.resources.custom_clients import finnhub_client
from app.finapp.solids.extract_data import consume_api
from pathlib import Path
# Mode definitions allow you to configure the behavior of your pipelines and solids at execution
# time. For hints on creating modes in Dagster, see our documentation overview on Modes and
# Resources: https://docs.dagster.io/overview/modes-resources-presets/modes-resources

path = os.path.join(Path(__file__).parent, 'config_pipelines', 'data_stocks.yaml')
MODE = ModeDefinition(name="dev",
                      resource_defs={'finnhub_client' : finnhub_client},
                      )
PRESET = PresetDefinition.from_files(name='data_stock',
                                     config_files=[path],
                                     mode='dev'
                          )


@pipeline(mode_defs=[MODE], preset_defs=[PRESET])
def forescating_market():
    """
    A pipeline definition. This example pipeline has a single solid.

    For more hints on writing Dagster pipelines, see our documentation overview on Pipelines:
    https://docs.dagster.io/overview/solids-pipelines/pipelines
    """
    consume_api()