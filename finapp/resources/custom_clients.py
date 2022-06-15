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
    try:
        api_key = os.getenv('FINNUB_KEY')
    except Exception as e:
        api_key = config('FINNUB_KEY', api_key)
    if api_key is not None:
        client = finnhub.Client(api_key)
    else:
        raise Exception('FINNUB_KEY the env varible is empty or it does not exist')
    return client
