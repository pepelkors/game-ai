import tensorflow as tf
from tensorflow import keras
from keras import layers

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
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

