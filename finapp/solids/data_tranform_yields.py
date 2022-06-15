from dagster import job, make_values_resource, op
import pandas as pd
import os

@op(required_resource_keys={"values"})
def get_candada_data_yield(context) -> pd.DataFrame:
    path = context.resources.values['cadatayieldsall']
    df = pd.read_csv(path, on_bad_lines='skip')

    return df


@op()
def taranfrom_data(df)-> pd.DataFrame:
    df = df.set_index('date')
    for column in df.columns:
        df[column] = df[column].apply(pd.to_numeric, errors='coerce')

    df = df.dropna(how='all', axis=0)

    print(df)
    return df





@op()
def get_data_transform(data)-> pd.DataFrame:
    print("this is test to work with data")
    #data = get_candada_data_yield()


    return data

@op()
def save_clean_data(df):
    #path_file = os.path.dirname(__file__)
    path_file = 'finapp/local_transferm_data'
    folder = os.path.abspath(os.path.join(path_file, "..", "data"))
    filename = os.path.join("(finapp/local_transferm_data", 'cleaned_data_yield_all' + ".csv")
    print(filename)
    writer = df.to_csv(filename, index= False)



@job(resource_defs={"values": make_values_resource(usadata=str, cadatayieldsall=str, cadata=str)})
def get_ingestion_data_yield():

    df= get_candada_data_yield()

    df = taranfrom_data(df)
    ##save_clean_data(df)


if __name__ == "__main__":
    result = get_ingestion_data_yield.execute_in_process(
        run_config={"resources": {"values": {"config": {"usadata": "", "cadatayieldsall":'finapp/local_data/bond_yields_all_noheader.csv', "cadata": 'finapp/local_data/bond_yields_all.csv'}}}}

    )
