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

#gamepad = 

# Move the Project Heartbeat window to the front
# ? not needed because sets foreground
# hb_window.maximize()


def selectLevel():
    print("i dont know what you want me to do")
    # this is where we need to hand stuff outside of this program i thin
    # for now we will manually have it exit and move onto the next level
    # right right enter down enter
    ui.press("right")
    ui.press("right")
    ui.press("enter")
    ui.press("down")
    ui.press("enter")
    print("level selected")
    # await for level start
    time.sleep(1)
    ui.press("esc")


def main():

    # doing some time management
    prevTime = time.time()
    with mss.mss() as sct:
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
            scoreMeter = scoreFrame(img)

            # Display the game window
            cv2.imshow("Game Window", edges)
            cv2.imshow("accuracyMeter Window", accuracyMeter)
            cv2.imshow("scoreMeter Window", scoreMeter)
            # Time management
            prevTime = time.time()

            # # press the "x" numpad with vgamepad
            # gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            # gamepad.update()
            # time.sleep(0.05)
            # gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            # gamepad.update()

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Exited with q")
                break


if(__name__ == "__main__"):
    # Find the Project Heartbeat window by its title
    hb_window = gw.getWindowsWithTitle("Project Heartbeat (DEBUG)")[0]
    win32gui.SetForegroundWindow(hb_window._hWnd)
    # Activate the Project Heartbeat window
    hb_window.activate()
    #hb_window.size = (960, 540)
    #?maintian a 16 by 9 aspect ratio window
    tw = hb_window.width
    th = (tw/16)*9
    hb_window.size = (tw, th)
    
    #run main loop
    main()
    # release all windows
    cv2.destroyAllWindows()