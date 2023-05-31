# this is where the ai actually plays games and learns?

from tensorflow.keras.models import load_model
import numpy as np

# load the trained model from the models folder
# ask the user for the name of the model they want to use
try:
    model = load_model(
        f'models/{input("What model would you like to use?")}.h5')
except:
    print("That model does not exist")
    exit()

# we need to take heartbeat processor frames and return inputs to use
