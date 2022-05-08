from dagster import execute_pipeline

from finapp.pipelines.bond_prices import bond_prices_pipeline
from finapp.pipelines.forescating_market import forescating_market

if __name__=='__main__':
    # debugging pipeline
    execute_pipeline(pipeline=bond_prices_pipeline, preset='bond_price')
    print('hi')

    #