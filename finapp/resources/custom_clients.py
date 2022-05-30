import os

from dagster import resource, Field, Noneable
import finnhub
from decouple import config

@resource(
    description="This resource provides a finnhub client",
    config_schema={'api_key': Noneable(str)}
)
def finnhub_client(context):
    """
    Returns: A finnhub client.
    """
    api_key = config('FINNUB_KEY', None)
    try:
        client = finnhub.Client(api_key)
    except Exception as e:
        raise e
    return client