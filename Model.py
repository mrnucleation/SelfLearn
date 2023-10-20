#from tensorflow import keras
import keras_core as keras

def getexploremodel():
    model = keras.models.Sequential(
        [
            keras.Input(shape=(5,)),
            keras.layers.Dense(7, activation='relu'),
            keras.layers.Dense(7, activation='relu'),
            keras.layers.Dense(7, activation='relu'),
            keras.layers.Dense(6, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ]
    )
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model