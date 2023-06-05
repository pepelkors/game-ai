# this is a class that will be used to process and format data from the game ProjectHeartbeat
# project heartbeat is a rhythm game, where the player must press the correct key at the correct time
# the objective of this class is to simplify on screen data into a format that can be used by a neural network

# this class will first access the screen to grab frames from the game
# next step is to process the frames to get the position

import threading
from utils import *
import time
import cv2
import mss
import numpy as np
import pygetwindow as gw
import win32gui

import datetime


xboxController = XboxController()
openThreads: list[threading.Thread] = []
ss = []
inputArr = []
recording = False
safe = True


def main():
    global recording, safe
    prevTime = 0
    with mss.mss() as sct:
        i = 0
        while True:
            tempTime = round(time.time()*1000)
            if ((tempTime - prevTime) < 50):
                time.sleep((tempTime - prevTime)/1000)

            prevTime = tempTime
            # Get the position and size of the Project Heartbeat window
            game_window = {"top": hb_window.top+30, "left": hb_window.left +
                           8, "width": hb_window.width-16, "height": hb_window.height-38}
            screenshot = sct.grab(game_window)

            # Convert the screenshot to a NumPy array
            img = np.array(screenshot)
            # shrink frame to 540 * 960 - 16*38
            img = cv2.resize(img, (256, 144))
            # Process the frame

            edges, meanValue = edgeFrame(img)
            accuracyMeter = accuracyFrame(img)
            scoreMeter = scoreFrame(img)
            cv2.imshow("Game Window", edges)
            cv2.imshow("accuracyMeter Window", accuracyMeter)
            cv2.imshow("scoreMeter Window", scoreMeter)

            if (recording):
                # Display the game window
                inputs = xboxController.read()
                inputArr.append(inputs)
                ss.append(edges)

            if (xboxController.dump()):
                if (not recording):
                    recording = True
                    # clear arrays
                    ss = []
                    inputArr = []
                    print("recording")
                else:
                    recording = False
                    print("stopped recording")
                    if (safe):
                        safe = False
                        temp = threading.Thread(
                            target=saveData, args=(ss, inputArr, i))
                        temp.start()
                        openThreads.append(temp)
                        i += 1
            if cv2.waitKey(20) == ord("q"):
                print("Exited with q")
                break


def saveData(edges, inputArr, index):
    global safe
    start_time = datetime.datetime.now()
    np.savez_compressed(
        f"./recordings/trainingData{str(index)}.npz", edges=edges, inputs=inputArr)
    elapsed = datetime.datetime.now() - start_time
    print(f"Numpy array saved in trainingData{str(index)}.npz in " + str(
        int(elapsed.total_seconds()*1000)) + "ms")
    safe = True


if (__name__ == "__main__"):
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

    # run main loop
    main()
    for thread in openThreads:
        thread.join()
    # release all windows
    cv2.destroyAllWindows()
