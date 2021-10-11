from dagster import repository

from finapp.pipelines.forescating_market import forescating_market
from finapp.schedules.my_hourly_schedule import my_hourly_schedule
from finapp.sensors.my_sensor import my_sensor


@repository
def finapp():
    """
    The repository definition for this finapp Dagster repository.

    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """
    pipelines = [forescating_market]
    schedules = [my_hourly_schedule]
    sensors = [my_sensor]

    return pipelines + schedules + sensors
