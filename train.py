import tensorflow as tf
from tensorflow import keras
from keras import layers
from sklearn.model_selection import train_test_split
import numpy as np
import os

# read all the file names from the recordings folder
recordings = os.listdir('recordings')


# for i in recordings[1:]:
#     print(i)
#     # read the recordings
#
#     allSC = np.append(raw['edges'], allSC)
#     inp = np.append(raw['inputs'], inp)
#     del (raw)


# Define the CNN model
model = keras.Sequential([
    layers.Conv2D(32, kernel_size=(4, 4), activation='sigmoid',
                  input_shape=(144, 256, 1)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(256, activation='sigmoid'),
    layers.Dense(64, activation='sigmoid'),
    layers.Dense(11, activation='relu')
])

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])

for i in range(len(recordings)):
    raw = np.load(f'recordings/{recordings[i]}')
    frames = raw['edges']
    inp = raw['inputs']

    print(np.shape(inp))
    frames = frames.astype('float32') / 255.0  # Normalize pixel values
    frames = np.reshape(frames, (frames.shape[0], 144, 256, 1))

    buttons_encoded = inp

    # Use validation_split argument for automatic data split
    model.fit(frames, buttons_encoded, batch_size=32,
              epochs=10, validation_split=0.2)

    model.save(f'models/{i}.h5')

# Print the model summary
model.summary()


# Print the model summary
model.summary()
