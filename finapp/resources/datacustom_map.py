import os

from dagster import resource, Field, Noneable
#from decouple import config

@resource(
    description="This resource provides a finnhub client",
    config_schema={'looks': Noneable(str)}
)
def canadadata(context):

     try:
         print("this is resource")
        client = "finnhub.Client(api_key)"
    except Exception as e:
        raise e
    return client












