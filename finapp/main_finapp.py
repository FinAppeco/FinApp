from finapp.pipelines.forescast_bond_price_canada import forescast_bond_price_canada_api
from finapp.resources.custom_clients import finnhub_client
from finapp.resources.get_config_jobs import PipelineConfiguration

test_config = PipelineConfiguration(name='forescast_bond_price_canada', resource={'finnhub_client': finnhub_client})

if __name__=='__main__':
    # debugging pipeline
    forescast_bond_price_canada_api.execute_in_process(
        run_config=test_config.get_preset(name_yaml='bond_prices_canada.yml'))
    print("Success")
