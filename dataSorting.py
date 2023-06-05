# this file takes in recording files, and removes the frames that do not have any inputs associated

# get just one recording, start with 0

import os
import numpy as np

recordings = os.listdir('recordings')
recording = np.load(f'recordings/{recordings[0]}')

# now to iterate through the recording and remove the frames that have an input set that sums to 0
for i in recordings:
    print(i)
    # read the recordings
    raw = np.load(f'recordings/{i}')
    edges = raw['edges']
    print(len(edges))

    inputs = raw['inputs']

    # Create a modified recording file in the modifiedRecordings folder

    print(np.shape(edges))
    frameRemoved = 0
    for j in range(len(edges)-1, -1, -1):
        currentFrame = edges[j]
        # print(np.shape(currentFrame))
        currentInputs = inputs[j]
        # now is where things change from the replay.py file
        # if the sum of the inputs is 0, then we remove the frame
        if np.sum(currentInputs) == 0:
            edges = np.delete(edges, j, 0)
            inputs = np.delete(inputs, j, 0)
            # for now just print that you removed a frame
            frameRemoved += 1
    print(f'Frames removed: {frameRemoved}')
    # now to save the modified recording
    np.savez_compressed(f'modifiedRecordings/{i}', edges=edges, inputs=inputs)
    print(f'New recording saved as modifiedRecordings/{i}')
