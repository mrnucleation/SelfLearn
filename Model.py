#from tensorflow import keras
import keras_core as keras

def getexploremodel():
    model = keras.models.Sequential(
        [
            keras.layers.Dense(32, activation='relu', input_shape=(1,)),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(1, activation='relu')
        ]
    )
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model