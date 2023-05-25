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
import vgamepad as vg
import keyboard

# Find the Project Heartbeat window by its title
hb_window = gw.getWindowsWithTitle("Project Heartbeat (DEBUG)")[0]
win32gui.SetForegroundWindow(hb_window._hWnd)
# Activate the Project Heartbeat window
hb_window.activate()


gamepad = vg.VX360Gamepad()

# Move the Project Heartbeat window to the front
# ? not needed because sets foreground
# hb_window.maximize()

# Get the position and size of the Project Heartbeat window
left, top, width, height = hb_window.left, hb_window.top, hb_window.width, hb_window.height

# Print the window position and size
print("Window Position:", left, top)
print("Window Size:", width, height)

game_window = {"top": top, "left": left, "width": width, "height": height}


def processFrame(frame):
    # change size to 960 x 540
    frame = cv2.resize(frame, (960, 540))

    processedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # for now we are just turning it into greyscale and do some edge detection
    processedImage = cv2.Canny(processedImage, threshold1=200, threshold2=300)
    return processedImage


def accuracyMeter(frame):
    # accuracy meter is 1/3 of the screen in the center, but only the bottom 1/15th of the screen
    accuracyImage = frame[int(frame.shape[0] * (13/15)):frame.shape[0],
                          int(frame.shape[1] * (1/3)):int(frame.shape[1] * (2/3))]
    # processing to only have white pixels exist in the image
    accuracyImage = cv2.cvtColor(accuracyImage, cv2.COLOR_BGR2GRAY)
    # create an image with only white pixels
    whitePixels = np.where(accuracyImage == 255)

    # find the x coordinate center of the white pixels
    whitePixCenter = np.mean(whitePixels[1])

    # now we need to find how far from the actual center the white pixels are
    # 160 is the x center of the image, so we subtract the white pixel center from 160 and take abs value
    distFromCenter = abs(160 - whitePixCenter)
    return whitePixCenter, np.mean(accuracyImage)


def selectLevel():
    print("press a key to do shit")

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
        oldPixelCenter = 0
        while True:
            # Capture the game window
            screenshot = sct.grab(game_window)

            # print("Capture screenshot")

            # Convert the screenshot to a NumPy array
            img = np.array(screenshot)

            # Process the frame
            whitePixelCenter, meanValue = accuracyMeter(img)
            # Calculate the change in white pixel center. if it moved towards zero, print "better"
            deltaPixelCenter = whitePixelCenter - oldPixelCenter
            if deltaPixelCenter < 0:
                print("better")
                print(deltaPixelCenter)
            if deltaPixelCenter > 0:
                print("worse")
                print(deltaPixelCenter)

            oldPixelCenter = whitePixelCenter
            # print the mean value of the image
            # print(meanValue)
            # if it is below 10, the level ended
            if meanValue <= 0:
                print("Level ended")
                # this is where we need to hand stuff outside of this program
                selectLevel()
            # Display the game window
            cv2.imshow("Game Window", img)

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
