from dagster import op, Noneable, Out, Field, get_dagster_logger
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

logger = get_dagster_logger()


@op(config_schema={'batch_size': Field(Noneable(int), default_value=1, is_required=False),
                   'nb_epoch': Field(Noneable(int), default_value=10, is_required=False),
                   'neurons': Field(Noneable(int), default_value=10, is_required=False)})
def fit_lstm(context, data):
    batch_size = context.solid_config["batch_size"]
    nb_epoch = context.solid_config["nb_epoch"]
    neurons = context.solid_config["neurons"]

    train = data["train_scaled"]
    X, y = train[:, 0:-1], train[:, -1]
    X = X.reshape(X.shape[0], 1, X.shape[1])
    model = Sequential()
    model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    for i in range(nb_epoch):
        model.fit(X, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
        model.reset_states()

    train_reshaped = train[:, 0].reshape(len(train), 1, 1)
    model.predict(train_reshaped, batch_size=1)
    # Export the model to a local SavedModel directory
    bucket_path_model = 'gs://finapp/models/' + context.op.name
    export_path = tf.keras.models.save_model(model, bucket_path_model)
    logger.info("Model exported to : " + bucket_path_model)
    return model
