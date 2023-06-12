from utils import XboxController
import cv2
import numpy as np
import os

# read all the file names from the recordings folder
recordings = os.listdir('modifiedRecordings')
gamepad = XboxController()

recordings.sort()

for i in recordings:
    print(i)
    # read the recordings
    raw = np.load(f'modifiedRecordings/{i}')
    edges = raw['edges']
    print(len(edges))

    inputs = raw['inputs']

    print(np.shape(edges))

    for j in range(len(edges)):
        currentFrame = edges[j]
        # print(np.shape(currentFrame))
        currentInputs = inputs[j]
        currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2RGB)
        colors = [(0, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (128, 0, 255), (128,
                                                                                        0, 255), (255, 0, 255), (255, 255, 0), (255, 255, 0), (255, 255, 0), (255, 255, 0)]
        for k in range(len(currentInputs)):
            if currentInputs[k] == 1:
                size = 32
                pos = k*size
                cv2.rectangle(currentFrame, (pos, 0),
                              (pos+size, size), colors[k], -1)

        cv2.imshow('edges', currentFrame)
        if cv2.waitKey(20) == ord("q"):
            print("Exited with q")
            break

cv2.destroyAllWindows()
