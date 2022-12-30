from datetime import datetime

from dagster import schedule

from finapp.pipelines.bond_prices import get_bond_prices_api, config_bonds


@schedule(job=get_bond_prices_api, cron_schedule="0 0 * * *")
def my_hourly_schedule(_context):
    """
    A schedule definition. This example schedule runs a pipeline every hour.

    For more hints on scheduling pipeline runs in Dagster, see our documentation overview on
    Schedules:
    https://docs.dagster.io/overview/schedules-sensors/schedules
    """
    run_config = config_bonds
    return run_config
