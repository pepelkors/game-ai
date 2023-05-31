import tensorflow as tf
from tensorflow import keras
from keras import layers
from utils import XboxController
import cv2
import numpy as np
import os

# read all the file names from the recordings folder
recordings = os.listdir('recordings')
gamepad = XboxController()

recordings.sort()
allSC = []
inp = []
for i in recordings[1:]:
    print(i)
    # read the recordings
    raw = np.load(f'recordings/{i}')
    allSC = np.append(raw['edges'], allSC)
    inp = np.append(raw['inputs'], inp)
    del (raw)


# Define the CNN model
model = keras.Sequential()

# Add Convolutional layers
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(502, 944, 1)))
model.add(layers.MaxPooling2D((2, 2)))

# Add more Convolutional layers as needed
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# Flatten layer
model.add(layers.Flatten())

# Add Dense layers
model.add(layers.Dense(128, activation='relu'))

# Output layer
model.add(layers.Dense(8, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])
validate = np.load(f'recordings/{recordings[0]}')
model.fit(allSC, inp, epochs=10, batch_size=32,
          validation_data=(validate["edges"], validate["inputs"]))

train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
test_dataset = tf.data.Dataset.from_tensor_slices((test_data, test_labels))


# save model to the saved model folder
# ask the user what they would like to name the model, and save it in models folder
model.save(f'models/{input("What would you like to name the model?")}.h5')

# Print the model summary
model.summary()
