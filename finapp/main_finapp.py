from finapp.pipelines.bond_prices import get_bond_prices_api
from finapp.resources.custom_clients import finnhub_client
from finapp.resources.get_config_jobs import PipelineConfiguration

test_config = PipelineConfiguration(name='bond_price_prediction_api', resource={'finnhub_client': finnhub_client})

if __name__=='__main__':
    # debugging pipeline
    get_bond_prices_api.execute_in_process(run_config=test_config.get_preset(name_yaml='bond_price.yaml'))
    print("Success")

