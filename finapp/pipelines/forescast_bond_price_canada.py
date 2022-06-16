from dagster import graph

from finapp.resources.get_config_jobs import PipelineConfiguration
from finapp.solids.extract_data import get_bond_price_canada
from finapp.solids.models_data import fit_lstm

from finapp.solids.transform_data import difference, timeseries_to_supervised, split_data, scale, split_outputs

test_config = PipelineConfiguration(name='forescast_bond_price_canada_api_2')


@graph()
def forescast_bond_price_canada():
    df = get_bond_price_canada()
    df1 = split_outputs(df)
    # model1
    df1 = difference.alias("CDN_AVG_1YTO3Y_AVG_difference")(df1)
    df1 = timeseries_to_supervised.alias("CDN_AVG_1YTO3Y_AVG_timeseries_to_supervised")(df1)
    dict_data1 = split_data.alias("CDN_AVG_1YTO3Y_AVG_split_data")(df1)
    dict_scaler_data1 = scale.alias("CDN_AVG_1YTO3Y_AVG_scale")(dict_data1)
    fit_lstm.alias('CDN_AVG_1YTO3Y_AVG_fit_lstm')(dict_scaler_data1)
    # # model2
    # df2 = difference.alias("BD_CDN_2YR_DQ_YLD_difference")(df2)
    # df2 = timeseries_to_supervised.alias("BD_CDN_2YR_DQ_YLD_timeseries_to_supervised")(df2)
    # dict_data2 = split_data.alias("BD_CDN_2YR_DQ_YLD_split_data")(df2)
    # dict_scaler_data2 = scale.alias("BD_CDN_2YR_DQ_YLD_scale")(dict_data2)
    # fit_lstm.alias('BD_CDN_2YR_DQ_YLD_fit_lstm')(dict_scaler_data2)


config_bonds = test_config.get_preset(name_yaml='bond_prices_canada.yml')

forescast_bond_price_canada_api_2 = forescast_bond_price_canada.to_job(resource_defs=test_config.get_io_managers(),
                                                                       name="forescast_bond_price_canada_api_2")

# @job(name='forescast_bond_price_canada_api',
#      resource_defs=test_config.get_io_managers(),
#      description="Pipeline for bond prices of canada",
#      config=config_bonds)
# def forescast_bond_price_canada_api():
#     return forescast_bond_price_canada
