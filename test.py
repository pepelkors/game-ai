import os
import numpy as np


recordings = os.listdir('recordings')

# mixing variable
mixingRate = 0.5

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

# # now to iterate through the recording
# for i in recordings:
#     # we need to read the recording
#     raw = np.load(f'recordings/{i}')
#     edges = raw['edges']
#     inputs = raw['inputs']
#     # now to iterate through the inputs
#     for j in range(len(inputs)):
#         # if the sum of the inputs is 0, then we add the frame to the noInput list
#         if np.sum(inputs[j]) == 0:
#             noInput[0].append(edges[j])
#             noInput[1].append(inputs[j])
#         else:
#             for k in range(len(inputs[j])):
#                 if inputs[j][k] == 1:
#                     inputTuple[k][0].append(edges[j])
#                     inputTuple[k][1].append(inputs[j])
#                     break
#     print("recording " + i + " done")

# just read from the first recording in the file
raw = np.load(f'recordings/{recordings[0]}')
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
print("recording " + recordings[0] + " done")


# now we need to take all of our data and put it into one file. This needs to make the right "mix" of different inputs
mergedInputs = [[], []]
# we will just go with them in order
for bucket in inputTuple:
    # make a check that this isnt the last input, if that is the case, just end the loop
    if inputTuple.index(bucket) == len(inputTuple) - 1:
        break

    bucket

    # shuffle the bucket
    tempBucket = [[], []]
    length = len(bucket[0])
    indices = list(range(length))
    np.random.shuffle(indices)
    for i in indices:
        tempBucket[0].append(bucket[0][i])
        tempBucket[1].append(bucket[1][i])
        print(i)

    # now we need to mix the two buckets together
    # if the mixing percentage is greater than the percentage progressed in the current bucket, just add the frame
    # if the mixing percentage is less than the percentage progressed in the current bucket, then we need to add the frame from the next bucket
    finished = False
    indexx = 0
    while finished != True:
        # we need to check that we havent reached the end of our temp bucket
        if indexx >= len(tempBucket[0]) - 1:
            # we are done
            finished = True
            break
        # check if the mixing percentage is greater than the percentage progressed (measured by indexx)
        if mixingRate > (indexx / len(tempBucket[0])):
            # add the frame from the current bucket
            print(indexx)
            mergedInputs[0].append(tempBucket[0][indexx])
            mergedInputs[1].append(tempBucket[1][indexx])
            indexx += 1
        else:
            probability = (indexx/len(tempBucket))
            result = np.random.random() < probability
            print(result)
            if result == True:
                # add the frame from the next bucket
                mergedInputs[0].append(bucket[0][indexx])
                mergedInputs[1].append(bucket[1][indexx])
            else:
                # add the frame from the current bucket
                mergedInputs[0].append(tempBucket[0][indexx])
                mergedInputs[1].append(tempBucket[1][indexx])
            indexx += 1

# save the inputs
np.savez_compressed(f'modifiedRecordings/mergedInputs',
                    edges=mergedInputs[0], inputs=mergedInputs[1])

# now to save the modified recordings
# if they dont have any information in the input, then we dont save them
# b = 0
# for i in range(len(inputTuple)):
#     if len(inputTuple[i][0]) != 0:
#         np.savez_compressed(
#             f'modifiedRecordings/recording{i+1}', edges=inputTuple[i][0], inputs=inputTuple[i][1])
#         print(f'New recording saved as modifiedRecordings/recording{i+1}')
#         b = i
# if len(noInput[0]) != 0:
#     np.savez_compressed(f'modifiedRecordings/recording{b+2}',
#                         edges=noInput[0], inputs=noInput[1])
#     print(
#         f'New recording saved as modifiedRecordings/recording{b+2} (no input)')
# print('Done')
