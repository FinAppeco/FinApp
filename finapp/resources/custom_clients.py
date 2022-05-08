from dagster import resource, Field, Noneable
import finnhub
from decouple import config

@resource(
    description="This resource provides a praw reddit instance",
    config_schema={'api_key': Noneable(str)}
)
def finnhub_client(context):
    """
    Args:
        config: A configuration containing the fields in GCS_CLIENT_CONFIG.

    Returns: A GCS client.
    """
    api_key = config('FINNUB_KEY', None)
    try:
        client = finnhub.Client(api_key)
    except Exception as e:
        raise e
    return client