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
model = keras.Sequential()

model = keras.Sequential([
    layers.Conv2D(32, kernel_size=(4, 4), activation='relu',
                  input_shape=(144, 256, 1)),
    layers.MaxPooling2D(pool_size=(8, 8)),
    layers.Flatten(),
    layers.Dense(48, activation='relu'),
    # Assuming you want 11 outputs with sigmoid activation
    layers.Dense(11, activation='sigmoid')
])

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])


for i in range(len(recordings)):
    raw = np.load(f'recordings/{recordings[i]}')
    frames = raw['edges']
    inp = raw['inputs']
    print(np.shape(inp))
    frames = frames.astype('float32') / 255.0  # Normalize pixel values
    # Reshape to (samples, height, width, channels)
    frames = np.reshape(frames, (frames.shape[0], 144, 256, 1))
    buttons_encoded = inp
    frames_train, frames_val, buttons_train, buttons_val = train_test_split(
        frames, buttons_encoded, test_size=0.2)
    print(np.shape(frames_train))
    print(np.shape(buttons_train))
    model.fit(frames_train, buttons_train, batch_size=32,
              epochs=10, validation_data=(frames_val, buttons_val))
    model.save(f'models/{i}.h5')


# Print the model summary
model.summary()
