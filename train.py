import tensorflow as tf
from tensorflow import keras
from keras import layers
from sklearn.model_selection import train_test_split
import numpy as np
import os

# read all the file names from the recordings folder
recordings = os.listdir('modifiedRecordings')


# for i in recordings[1:]:
#     print(i)
#     # read the recordings
#
#     allSC = np.append(raw['edges'], allSC)
#     inp = np.append(raw['inputs'], inp)
#     del (raw)

input_shape = (144, 256, 1)
# Define the CNN model
model = keras.Sequential()
# Add convolutional layers
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

# Flatten the output of the convolutional layers
model.add(layers.Flatten())

# Add LSTM layers
model.add(layers.Reshape((256, 240)))  # Reshape to match LSTM input shape
model.add(layers.LSTM(64, return_sequences=True))
model.add(layers.LSTM(64))

model.add(layers.Dense(11, activation='sigmoid'))


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
