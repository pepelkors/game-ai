import threading
from utils import XboxController
import time
import cv2
import mss
import numpy as np
import pygetwindow as gw
import win32gui
import os

import datetime 


#read all the file names from the recordings folder

recordings = os.listdir('recordings')
gamepad = XboxController()

recordings.sort()

for i in recordings:
    print(i)
    
    #read the recordings
    
    raw = np.load(f'recordings/{i}')
    edges = raw['edges']
    print(len(edges))
    inputs = raw['inputs']
    for j in range(len(edges)):
        #time.sleep(0.1)
        print(np.shape(edges[j]))
        current = edges[j]
        current = cv2.cvtColor(current, cv2.COLOR_BGR2RGB)
        
        cv2.imshow('edges', edges[j])
        
        if cv2.waitKey(100) == ord("q"):
            print("Exited with q")
            break

cv2.destroyAllWindows()