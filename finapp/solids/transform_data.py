from dagster import op, Noneable, Out, Field, get_dagster_logger
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

logger = get_dagster_logger()


@op(out={"out1": Out(), "out2": Out()})
def split_outputs(context, dataset):
    dataset.set_index("date", inplace=True)
    dataset1 = dataset['CDN_AVG_1YTO3Y_AVG']
    dataset2 = dataset['BD_CDN_2YR_DQ_YLD']
    return dataset1, dataset2


@op(config_schema={'interval': Field(Noneable(int), default_value=1, is_required=False)})
def difference(context, dataset):
    interval = context.solid_config["interval"]
    dataset = dataset.values
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return pd.Series(diff)


@op(config_schema={'lag': Field(Noneable(int), default_value=1, is_required=False)})
def timeseries_to_supervised(context, data):
    lag = context.solid_config["lag"]
    df = pd.DataFrame(data)
    columns = [df.shift(i) for i in range(1, lag + 1)]
    columns.append(df)
    df = pd.concat(columns, axis=1)
    df.fillna(0, inplace=True)
    return df


@op(config_schema={'test_percentage': Field(Noneable(int),
                                            default_value=1,
                                            is_required=False,
                                            description="Percentage [0,100] of data used for testing")})
def split_data(context, data):
    test_percentage = context.solid_config["test_percentage"]

    # split data into train and test-sets
    index = int(np.floor(len(data) * (test_percentage / 100)))
    train, test = data[0:-index], data[-index:]

    return {
        'train': train,
        'test': test
    }


@op(config_schema={'lag': Field(Noneable(int), default_value=1, is_required=False)})
def scale(context, data):
    train = data['train'].values
    test = data['test'].values
    # fit scaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(train)
    # transform train
    train = train.reshape(train.shape[0], train.shape[1])
    train_scaled = scaler.transform(train)
    # transform test
    test = test.reshape(test.shape[0], test.shape[1])
    test_scaled = scaler.transform(test)

    # save the scaler

    model_filename = 'rf_model.joblib'
    joblib.dump(train_scaled, model_filename)

    bucket = storage.Client().bucket(bucket_id)
    blob = bucket.blob('{}/{}'.format(
        bucket_path,
        model_filename))
    blob.upload_from_filename(model_filename)
    return {'scaler': scaler,
            'train_scaled': train_scaled,
            'test_scaled': test_scaled
            }