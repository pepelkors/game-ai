# this is a class that will be used to process and format data from the game ProjectHeartbeat
#project heartbeat is a rhythm game, where the player must press the correct key at the correct time
#the objective of this class is to simplify on screen data into a format that can be used by a neural network

#this class will first access the screen to grab frames from the game
#next step is to process the frames to get the position


import time
import cv2
import mss
import numpy as np
import pygetwindow as gw
import pyautogui as ui
import win32gui
import vgamepad as vg

# Find the Project Heartbeat window by its title
hb_window = gw.getWindowsWithTitle("Project Heartbeat (DEBUG)")[0]
win32gui.SetForegroundWindow(hb_window._hWnd)
# Activate the Project Heartbeat window
hb_window.activate()
hb_window.size = (960, 540)



gamepad = vg.VX360Gamepad()

# Move the Project Heartbeat window to the front
#? not needed because sets foreground
#hb_window.maximize()



def edgeFrame(frame, window):    
    # change size to 960 x 540
    processedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # for now we are just turning it into greyscale and do some edge detection
    processedImage = cv2.Canny(processedImage, threshold1=200, threshold2=300)
    
    meanValue = np.mean(frame)
    return processedImage, meanValue

def accuracyFrame(frame, window):
    # accuracy meter is 1/3 of the screen in the center, but only the bottom 1/15th of the screen
    print(frame.shape)
    print(window["top"])
    print(window["left"])
    #accuracyImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    accuracyImage = frame[frame.shape[0]-30: frame.shape[0],frame.shape[1]-630:frame.shape[1]-315]
    return accuracyImage
    # processing to only have white pixels exist in the image
    
    
    
    # create an image with only white pixels
    #whitePixels = np.where(accuracyImage == 255)
    return accuracyImage
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
    #await for level start
    time.sleep(1)
    ui.press("esc")
    

def main():
    
    # doing some time management
    prevTime = time.time()
    with mss.mss() as sct:
        while True:
            # Get the position and size of the Project Heartbeat window
            game_window = {"top": hb_window.top+30, "left": hb_window.left+8, "width": hb_window.width-16, "height": hb_window.height-38}
            screenshot = sct.grab(game_window)

            # Convert the screenshot to a NumPy array
            img = np.array(screenshot)

            # Process the frame
            edges, meanValue = edgeFrame(img, game_window)
            accuracyMeter= accuracyFrame(img, game_window)

            # Display the game window
            cv2.imshow("Game Window", edges)
            cv2.imshow("accuracyMeter Window", accuracyMeter)
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