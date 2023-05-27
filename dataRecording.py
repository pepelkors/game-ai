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
import win32gui
import vgamepad as vg


# Find the Project Heartbeat window by its title
hb_window = gw.getWindowsWithTitle("Project Heartbeat (DEBUG)")[0]
win32gui.SetForegroundWindow(hb_window._hWnd)
# Activate the Project Heartbeat window
hb_window.activate()
#hb_window.size = (960, 540)


gamepad = vg.VX360Gamepad()


def edgeFrame(frame):
    # change size to 960 x 540
    processedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # for now we are just turning it into greyscale and do some edge detection
    processedImage = cv2.Canny(processedImage, threshold1=200, threshold2=300)

    meanValue = np.mean(frame)
    return processedImage, meanValue

def accuracyFrame(frame):
    accuracyImage = frame[frame.shape[0]-23: frame.shape[0],
                          frame.shape[1]-612:frame.shape[1]-333]
    return accuracyImage

def scoreFrame(frame):
    # the score is in the top right corner
    scoreImage = frame[20: 45, frame.shape[1]-180: frame.shape[1]-55]
    return scoreImage


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


main()

# release all windows
cv2.destroyAllWindows()
