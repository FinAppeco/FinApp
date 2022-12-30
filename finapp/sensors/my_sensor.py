from dagster import RunRequest, sensor

from finapp.pipelines.bond_prices import config_bonds, get_bond_prices_api


@sensor(job=get_bond_prices_api)
def my_sensor(_context):
    """
    A sensor definition. This example sensor always requests a pipeline run at each sensor tick.

    For more hints on running pipelines with sensors in Dagster, see our documentation overview on
    Sensors:
    https://docs.dagster.io/overview/schedules-sensors/sensors
    """
    should_run = True
    if should_run:
        yield RunRequest(run_key=None, run_config=config_bonds)
