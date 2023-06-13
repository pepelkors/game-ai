import os
import numpy as np

recordings = os.listdir('recordings')

# create a 2d list for each input, there are 11 inputs
input1 = [[], []]
input2 = [[], []]
input3 = [[], []]
input4 = [[], []]
input5 = [[], []]
input6 = [[], []]
input7 = [[], []]
input8 = [[], []]
input9 = [[], []]
input10 = [[], []]
input11 = [[], []]
noInput = [[], []]
inputTuple = [input1, input2, input3, input4, input5,
              input6, input7, input8, input9, input10, input11]

# now to iterate through the recording
for i in recordings:
    # we need to read the recording
    raw = np.load(f'recordings/{i}')
    edges = raw['edges']
    inputs = raw['inputs']
    # now to iterate through the inputs
    for j in range(len(inputs)):
        # if the sum of the inputs is 0, then we add the frame to the noInput list
        if np.sum(inputs[j]) == 0:
            noInput[0].append(edges[j])
            noInput[1].append(inputs[j])
        else:
            for k in range(len(inputs[j])):
                if inputs[j][k] == 1:
                    inputTuple[k][0].append(edges[j])
                    inputTuple[k][1].append(inputs[j])
                    break
    print("recording " + i + " done")
# now to save the modified recordings
# if they dont have any information in the input, then we dont save them
b = 0
for i in range(len(inputTuple)):
    if len(inputTuple[i][0]) != 0:
        np.savez_compressed(
            f'modifiedRecordings/recording{i+1}', edges=inputTuple[i][0], inputs=inputTuple[i][1])
        print(f'New recording saved as modifiedRecordings/recording{i+1}')
        b = i
if len(noInput[0]) != 0:
    np.savez_compressed(f'modifiedRecordings/recording{b+2}',
                        edges=noInput[0], inputs=noInput[1])
    print(
        f'New recording saved as modifiedRecordings/recording{b+2} (no input)')
print('Done')
