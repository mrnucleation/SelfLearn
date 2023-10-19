#from tensorflow import keras
import keras_core as keras

def getexploremodel():
    model = keras.models.Sequential(
        [
            keras.Input(shape=(6,)),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(1, activation='relu')
        ]
    )
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model