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

# now to iterate through the recording
for i in recordings:
    # we need to read the recording
    raw = np.load(f'recordings/{i}')
    edges = raw['edges']
    inputs = raw['inputs']
    # now to iterate through the inputs
    for j in range(len(inputs)):
        # we need to see which input is active and therefore which ones to append to
        # there has got to be a better way but i cant find it
        if np.sum(inputs[j]) == 0:
            noInput[0].append(edges[j])
        else:
            if inputs[j][0] == 1:
                input1[0].append(edges[j])
                input1[1].append(inputs[j])
            if inputs[j][1] == 1:
                input2[0].append(edges[j])
                input2[1].append(inputs[j])
            if inputs[j][2] == 1:
                input3[0].append(edges[j])
                input3[1].append(inputs[j])
            if inputs[j][3] == 1:
                input4[0].append(edges[j])
                input4[1].append(inputs[j])
            if inputs[j][4] == 1:
                input5[0].append(edges[j])
                input5[1].append(inputs[j])
            if inputs[j][5] == 1:
                input6[0].append(edges[j])
                input6[1].append(inputs[j])
            if inputs[j][6] == 1:
                input7[0].append(edges[j])
                input7[1].append(inputs[j])
            if inputs[j][7] == 1:
                input8[0].append(edges[j])
                input8[1].append(inputs[j])
            if inputs[j][8] == 1:
                input9[0].append(edges[j])
                input9[1].append(inputs[j])
            if inputs[j][9] == 1:
                input10[0].append(edges[j])
                input10[1].append(inputs[j])
            if inputs[j][10] == 1:
                input11[0].append(edges[j])
                input11[1].append(inputs[j])
# now to save the modified recordings
np.savez_compressed(f'modifiedRecordings/input1',
                    edges=input1[0], inputs=input1[1])
np.savez_compressed(f'modifiedRecordings/input2',
                    edges=input2[0], inputs=input2[1])
np.savez_compressed(f'modifiedRecordings/input3',
                    edges=input3[0], inputs=input3[1])
np.savez_compressed(f'modifiedRecordings/input4',
                    edges=input4[0], inputs=input4[1])
np.savez_compressed(f'modifiedRecordings/input5',
                    edges=input5[0], inputs=input5[1])
np.savez_compressed(f'modifiedRecordings/input6',
                    edges=input6[0], inputs=input6[1])
np.savez_compressed(f'modifiedRecordings/input7',
                    edges=input7[0], inputs=input7[1])
np.savez_compressed(f'modifiedRecordings/input8',
                    edges=input8[0], inputs=input8[1])
np.savez_compressed(f'modifiedRecordings/input9',
                    edges=input9[0], inputs=input9[1])
np.savez_compressed(f'modifiedRecordings/input10',
                    edges=input10[0], inputs=input10[1])
np.savez_compressed(f'modifiedRecordings/input11',
                    edges=input11[0], inputs=input11[1])
np.savez_compressed(f'modifiedRecordings/noInput',
                    edges=noInput[0], inputs=noInput[1])

print('Done')
