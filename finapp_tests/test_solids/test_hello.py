from dagster import execute_solid



def test_hello():
    """
    This is an example test for a Dagster solid.

    For hints on how to test your Dagster solids, see our documentation tutorial on Testing:
    https://docs.dagster.io/tutorial/testable
    """
    result = execute_solid(None, mode_def=None)

    assert result.success
    assert result.output_value() == "Hello, Dagster!"
