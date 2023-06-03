# this file takes in recording files, and removes the frames that do not have any inputs associated

# get just one recording, start with 0

import os
import numpy as np

recordings = os.listdir('recordings')
recording = np.load(f'recordings/{recordings[0]}')

# now to iterate through the recording and remove the frames that have an input set that sums to 0
