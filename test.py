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
hb_window.size = (960, 540)


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

    return frame

def accuracyMeter(frame):
    # accuracy meter is 1/3 of the screen in the center, but only the bottom 1/15th of the screen
    accuracyImage = frame[928:929,180:360]
    # processing to only have white pixels exist in the image
    
    
    
    # create an image with only white pixels
    #whitePixels = np.where(accuracyImage == 255)
    return accuracyImage

def main():
    with mss.mss() as sct:
        while True:
            #if on start determine zero
            
            
            # Capture the game window
            screenshot = sct.grab(game_window)

            # print("Capture screenshot")

            # Convert the screenshot to a NumPy array
            img = np.array(screenshot)
            img = processFrame(img)
            # Process the frame
            whitePixel = accuracyMeter(img)

            cv2.imshow("Game Window", img)

  

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Exited with q")
                break


main()

# release all windows
cv2.destroyAllWindows()
