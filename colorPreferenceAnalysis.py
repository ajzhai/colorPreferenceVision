import numpy as np
import matplotlib.pyplot as plt

def fileToDict(filename):
    data = {}
    with open(filename, 'r') as f:
        for line in f:
            if line == '\n':
                break
            trialData = line.strip().split(' ')
            if len(trialData) == 4:
                color, loc, brkTime, tstPass = trialData
                brkTime = float(brkTime)
                if brkTime > 0.1 and brkTime < 10.23 and tstPass == 'True':
                    if color not in data.keys():
                        data[color] = [brkTime]
                    else:
                        data[color].append(brkTime)
            else:
                pass
    return data

def removeOutliers(nums):
    lower = np.mean(nums) - 3 * np.std(nums)
    upper = np.mean(nums) + 3 * np.std(nums)
    for i in range(len(nums) - 1, -1, -1):
        if nums[i] < lower or nums[i] > upper:
            nums.pop(i)
            
if __name__ == '__main__':
    output = fileToDict('/home/shimojolab/PsychopyExperiments/colorPrefData/testJuly30.txt')
    y = []
    for color in output.keys():
        removeOutliers(output[color])
        y.append(np.mean(output[color]))
        print color
        print np.mean(output[color])
    plt.subplots()[1].set_xticklabels([''] + output.keys())
    plt.bar(range(6), y, align='center')
    
    plt.show() 