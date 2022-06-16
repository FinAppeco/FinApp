from dagster import graph, job

from finapp.resources.get_config_jobs import PipelineConfiguration
from finapp.solids.extract_data import get_bond_price_canada
from finapp.solids.models_data import fit_lstm

from finapp.solids.transform_data import difference, timeseries_to_supervised, split_data, scale, split_outputs

test_config = PipelineConfiguration(name='bond_price_prediction_api')


@graph()
def get_bond_prices():
    """
    A graph definition to predict bond price
    """
    df = get_bond_price_canada()
    df1 = split_outputs(df)
    # model1
    df1 = difference(df1)
    df1 = timeseries_to_supervised(df1)
    dict_data1 = split_data(df1)
    dict_scaler_data1 = scale(dict_data1)
    fit_lstm(dict_scaler_data1)
    # model2
    # df2 = difference.alias("BD_CDN_2YR_DQ_YLD_difference")(df2)
    # df2 = timeseries_to_supervised.alias("BD_CDN_2YR_DQ_YLD_timeseries_to_supervised")(df2)
    # dict_data2 = split_data.alias("BD_CDN_2YR_DQ_YLD_split_data")(df2)
    # dict_scaler_data2 = scale.alias("BD_CDN_2YR_DQ_YLD_scale")(dict_data2)
    # fit_lstm.alias('BD_CDN_2YR_DQ_YLD_fit_lstm')(dict_scaler_data2)



config_bonds = test_config.get_preset(name_yaml='bond_price.yaml')
@job(name='get_bond_prices_api',
     resource_defs=test_config.get_io_managers(),
     description="Pipeline for bond prices",
     config=config_bonds)
def get_bond_prices_api():
    return get_bond_prices()

