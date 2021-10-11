from dagster import execute_pipeline
from finapp.pipelines.forescating_market import forescating_market

if __name__=='__main__':

    execute_pipeline(pipeline=forescating_market, preset='data_stock')
    print('hi')