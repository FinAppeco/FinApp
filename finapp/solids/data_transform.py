from dagster import job, make_values_resource, op
import pandas as pd
import os

@op(required_resource_keys={"values"})
def get_candada_data(context) -> pd.DataFrame:
    path =  context.resources.values['cadata']
    df = pd.read_csv(path, on_bad_lines='skip')

    return df

@op()
def get_data_transform(data):
    print("this is test to work with data")
    data['data39062'] = pd.to_numeric(pd.Series(data['V39062']), errors='coerce')
    data['data39056'] = pd.to_numeric(pd.Series(data['V39056']), errors='coerce')
    data['data39057'] = pd.to_numeric(pd.Series(data['V39057']), errors='coerce')
    print(data)
    data_df = data[['Date', 'data39062', 'data39056', 'data39057']]
    data_df = data_df.dropna()
    data_df = data_df.dropna(axis=0)

    print(data_df)

    return data_df

@op()
def save_clean_data(df):
    #path_file = os.path.dirname(__file__)
    path_file = 'finapp/local_transferm_data'
    folder = os.path.abspath(os.path.join(path_file, "..", "data"))
    filename = os.path.join(folder, 'cleaned_data' + ".csv")
    print(filename)
    writer = df.to_csv(filename, index= False)



@job(resource_defs={"values": make_values_resource(usadata=str, cadata=str)})
def get_ingestion_data():
    df = get_candada_data()
    df_data = get_data_transform(df)
    ##save_clean_data(df_data)


if __name__ == "__main__":
    print("Begin")
    result = get_ingestion_data.execute_in_process(
        run_config={"resources": {"values": {"config": {"usadata": "", "cadata": 'finapp/local_data/lookup3.csv'}}}}

    )
    print(result)
    print("end")




