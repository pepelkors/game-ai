# this is a class that will be used to process and format data from the game ProjectHeartbeat
# project heartbeat is a rhythm game, where the player must press the correct key at the correct time
# the objective of this class is to simplify on screen data into a format that can be used by a neural network

# this class will first access the screen to grab frames from the game
# next step is to process the frames to get the position


import time
import cv2
import mss
import numpy as np
import pygetwindow as gw
import pyautogui as ui
import win32gui
from utils import *
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

# this function will take in a frame and return what inputs are needed to be pressed
# this is the main function that will be used to process the frames


def performInference(frame):
    prediction = model.predict(frame)
    return prediction


def main():

    # doing some time management

    with mss.mss() as sct:
        previousX = 0
        while True:
            # Get the position and size of the Project Heartbeat window
            game_window = {"top": hb_window.top+30, "left": hb_window.left +
                           8, "width": hb_window.width-16, "height": hb_window.height-38}
            screenshot = sct.grab(game_window)

            # Convert the screenshot to a NumPy array
            img = np.array(screenshot)
            # shrink frame to 540 * 960 - 16*38
            img = cv2.resize(img, (944, 502))
            # Process the frame
            edges, meanValue = edgeFrame(img)
            accuracyMeter = accuracyFrame(img)
            averageX = whitePixelCenter(accuracyMeter)
            # round averagex and previousX to 2 decimal places
            deltaPixelCenter = averageX - previousX
            previousX = averageX
            scoreMeter = scoreFrame(img)

            # get the inputs from the model
            inputs = performInference(edges)
            # now to actually do something with them

            # Display the game window
            cv2.imshow("Game Window", edges)
            cv2.imshow("accuracyMeter Window", accuracyMeter)
            cv2.imshow("scoreMeter Window", scoreMeter)
            # Time management
            prevTime = time.time()

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Exited with q")
                break


if (__name__ == "__main__"):
    # load the model
    model = load_model('models/bwaa.h5')
    print("model loaded")
    # Find the Project Heartbeat window by its title
    hb_window = gw.getWindowsWithTitle("Project Heartbeat (DEBUG)")[0]
    win32gui.SetForegroundWindow(hb_window._hWnd)
    # Activate the Project Heartbeat window
    hb_window.activate()
    # hb_window.size = (960, 540)
    # ?maintian a 16 by 9 aspect ratio window
    tw = hb_window.width
    th = (tw/16)*9
    hb_window.size = (tw, th)
    prevTime = time.time()

    # run main loop
    main()
    # release all windows
    cv2.destroyAllWindows()
