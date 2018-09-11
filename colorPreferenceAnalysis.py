import numpy as np
import matplotlib.pyplot as plt
from scipy import stats 

SUBJECTS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '16', '17', '18', '19', '20', '21',
            '23', '25', '26', '27']  # '00' is myself

def breaksToDict(filename, includeAll):
    '''
    Reads in the breaking times from the first experiment and returns them as a dictionary
    where the color triplets are keys and the lists of breaking times are values. 
    The includeAll parameter indicates whether or not the trials that became definitely 
    visible should be included as max-duration breaking.
    '''
    data = {}
    with open(filename, 'r') as f:
        reading = False
        for line in f:
            if line == 'START1\n':
                reading = True
                continue
            elif line == 'END1\n':
                break
            if reading:
                trialData = line.strip().split(' ')
                color, loc, brkTime, tstPass = trialData
                brkTime = float(brkTime)
                passedScreen = brkTime > 0.3 and brkTime < 10.23
                if includeAll:
                    brkTime = min(brkTime, 10.23)
                    passedScreen = brkTime > 0.3 
                if passedScreen and tstPass == 'True':
                    if color not in data.keys():
                        data[color] = [brkTime]
                    else:
                        data[color].append(brkTime)
    return data
  
def breaksHistory(filename, includeAll):
    '''
    Reads in the breaking times from the first experiment and returns them as a list 
    of the mean breaking times for each 30-trial section in chronological order.
    The includeAll parameter indicates whether or not the trials that became definitely 
    visible should be included as max-duration breaking.
    '''
    data = []
    with open(filename, 'r') as f:
        reading = False
        trial = 0
        binSum, binCount = 0, 0
        for line in f:
            if line == 'START1\n':
                reading = True
                continue
            elif line == 'END1\n':
                break
            if reading:
                trialData = line.strip().split(' ')
                color, loc, brkTime, tstPass = trialData
                brkTime = float(brkTime)
                passedScreen = brkTime > 0.3 and brkTime < 10.23
                if includeAll:
                    brkTime = min(brkTime, 10.23)
                    passedScreen = brkTime > 0.3 
                if passedScreen and tstPass == 'True':
                    binSum += brkTime
                    binCount += 1
                if trial % 30 == 29:
                    data.append(binSum / binCount)
                    binSum = 0
                    binCount = 0
            trial += 1
    return data
   
   
def breakAvgsLR(filename):
    '''
    Reads in the breaking times from the first experiment and returns a tuple of the mean
    breaking times and standard deviations for each location. The format is as follows:
        
    (left mean, right mean, left stdev, right stdev)
    '''
    left, right = [], []
    with open(filename, 'r') as f:
        reading = False
        for line in f:
            if line == 'START1\n':
                reading = True
                continue
            elif line == 'END1\n':
                break
            if reading:
                trialData = line.strip().split(' ')
                color, loc, brkTime, tstPass = trialData
                brkTime = float(brkTime)
                if brkTime > 0.1 and brkTime < 10.23 and tstPass == 'True':
                    if float(loc) < 0:
                        left.append(brkTime)
                    else:
                        right.append(brkTime)
    return (np.mean(left), np.mean(right), np.std(left), np.std(right))

def prefsToDict(filename, colorsAreKeys):
    '''
    Reads in the preference rankings from the first experiment and returns them as a dictionary.
    If colorsAreKeys is passed as True, then the color triplets are the keys of the return
    dictionary. If False, then the preference ranks are the keys.
    '''
    data = {}
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == 'p':
                prefs = line.strip().split(' ')[1:]
                for pref in prefs:
                    if colorsAreKeys:
                        data[pref[:-1]] = int(pref[-1])
                    else:
                        data[int(pref[-1])] = pref[:-1]
    return data


def colorlist(filename):
    '''Returns colors used in first experiment in canonical rainbow order.'''
    data = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == 'p':
                prefs = line.strip().split(' ')[1:]
                for pref in prefs:
                    data.append(pref[:-1])
    return data
    
def removeOutliers(nums):
    '''Removes elements more than 3 standard deviations from the mean in an array of numbers.'''
    lower = np.mean(nums) - 3 * np.std(nums)
    upper = np.mean(nums) + 3 * np.std(nums)
    for i in range(len(nums) - 1, -1, -1):
        if nums[i] < lower or nums[i] > upper:
            nums.pop(i)

def calibrationHistory(filename):
    '''Returns the history of tilt magnitudes for both calibration staircases in chronological order.'''
    tiltMags1, tiltMags2 = [], []
    with open(filename, 'r') as f:
        reading = False
        for line in f:
            if line == 'CALIB\n':
                reading = True
                continue
            elif line == 'START2\n':
                break
            if reading:
                trialData = line.strip().split(' ')
                if len(trialData) > 1:
                    if trialData[0] == '0':
                        tiltMags1.append(abs(float(trialData[4][:-1])))
                    elif trialData[0] == '1':
                        tiltMags2.append(abs(float(trialData[4][:-1])))
    return tiltMags1, tiltMags2
    
def oriTaskAcc(filename, includeCalib):
    '''
    Reads in the orientation task results from the second experiment and returns them as a 
    dictionary where the keys are labels of the relevant configurations and the values are 
    proportions of correct responses.
    '''
    corrects = {'favSame': 0, 'favOpp': 0, 'leastFavSame': 0, 'leastFavOpp': 0}
    totals = {'favSame': 0, 'favOpp': 0, 'leastFavSame': 0, 'leastFavOpp': 0}
    topCorrects, bottomCorrects, tops, bottoms = 0, 0, 0, 0
    with open(filename, 'r') as f:
        reading = False
        for line in f:
            if (includeCalib and line == 'CALIB\n') or line == 'START2\n':
                reading = True
                continue
            elif line == 'END2\n':
                break
            if reading:
                trialData = line.strip().split(' ')
                if len(trialData) > 8:
                    calib = 1
                elif len(trialData) < 2:
                    continue
                else:
                    calib = 0
                popCol, popLoc, gabLoc, passedTask, visibility = trialData[0 + calib][1:-1], trialData[1 + calib][:-1], \
                                                                 trialData[2 + calib][:-1], trialData[5 + calib], trialData[6 + calib]
                if visibility == '0':
                    if popCol == '1':
                        if popLoc == gabLoc:
                            if passedTask == 'True':
                                corrects['favSame'] += 1
                            totals['favSame'] += 1
                        else:
                            if passedTask == 'True':
                                corrects['favOpp'] += 1
                            totals['favOpp'] += 1
                    else:
                        if popLoc == gabLoc:
                            if passedTask == 'True':
                                corrects['leastFavSame'] += 1
                            totals['leastFavSame'] += 1
                        else:
                            if passedTask == 'True':
                                corrects['leastFavOpp'] += 1
                            totals['leastFavOpp'] += 1
                    if float(gabLoc) > 0:
                        if passedTask == 'True':
                            topCorrects += 1
                        tops += 1
                    else:
                        if passedTask == 'True':
                            bottomCorrects += 1
                        bottoms += 1
    for c in corrects.keys():
        corrects[c] = float(corrects[c]) / totals[c]
    #print 'Total numbers of invisible trials: ' + str(totals)
    #print 'Accuracy in upper half: ' + str(topCorrects) + '/' + str(tops)
    #print 'Accuracy in lower half: ' + str(bottomCorrects) + '/' + str(bottoms)
    return corrects
    
    
def oriTaskSpd(filename):
    '''
    Reads in the orientation task results from the second experiment and returns them as a 
    dictionary where the keys are labels of the relevant configurations and the values are 
    mean response times.
    '''
    corrects = {'favSame': 0, 'favOpp': 0, 'leastFavSame': 0, 'leastFavOpp': 0}
    totals = {'favSame': 0, 'favOpp': 0, 'leastFavSame': 0, 'leastFavOpp': 0}
    topCorrects, bottomCorrects, tops, bottoms = 0, 0, 0, 0
    with open(filename, 'r') as f:
        reading = False
        for line in f:
            if line == 'START2\n':
                reading = True
                continue
            elif line == 'END2\n':
                break
            if reading:
                trialData = line.strip().split(' ')
                popCol, popLoc, gabLoc, reactTime, visibility = trialData[0][1:-1], trialData[1][:-1], \
                                                                trialData[2][:-1], trialData[4], trialData[6]
                if visibility == '0':
                    if popCol == '1':
                        if popLoc == gabLoc:
                            corrects['favSame'] += float(reactTime)
                            totals['favSame'] += 1
                        else:
                            corrects['favOpp'] += float(reactTime)
                            totals['favOpp'] += 1
                    else:
                        if popLoc == gabLoc:
                            corrects['leastFavSame'] += float(reactTime)
                            totals['leastFavSame'] += 1
                        else:
                            corrects['leastFavOpp'] += float(reactTime)
                            totals['leastFavOpp'] += 1
                    if float(gabLoc) > 0:
                        topCorrects += float(reactTime)
                        tops += 1
                    else:
                        bottomCorrects += float(reactTime)
                        bottoms += 1
    for c in corrects.keys():
        corrects[c] = corrects[c] / totals[c]
    print 'Total numbers of invisible trials: ' + str(totals)
    print 'Mean response time in upper half: ' + str(topCorrects / tops)
    print 'Mean response time in lower half: ' + str(bottomCorrects / bottoms)
    return corrects

def stimLocAcc(isVisible, filename):
    '''
    Reads in the orientation task results from the second experiment and returns the proportion
    of trials of the given reported visibility in which the target stimulus location was guessed correctly.
    '''
    correct, total = 0, 0
    with open(filename, 'r') as f:
        reading = False
        for line in f:
            if line == 'START2\n':
                reading = True
                continue
            elif line == 'END2\n':
                break
            if reading:
                trialData = line.strip().split(' ')
                popLoc, visibility, locSeen = trialData[1][:-1], trialData[6], trialData[7]
                if (not isVisible and visibility == '0') or (isVisible and not visibility == '0'):
                    if (popLoc[0] == '-' and locSeen == 'down') or (popLoc[0] == '0' and locSeen == 'up'):
                        correct += 1
                    total += 1 
    if total == 0:
        return -1
    return float(correct) / total
    
def plotST(inFile, outDir):
    '''
    Saves a bar chart of the mean suppression times for each color, ordered from most favorite to least
    favorite, from the given input file to the given output directory.
    '''
    bDict = breaksToDict(inFile, True)
    pDict = prefsToDict(inFile, True)
    colors, brkTimes, sds, prefs = [], [], [], []
    for color in bDict.keys():
        removeOutliers(bDict[color])
        colors.append(color)
        brkTimes.append(np.mean(bDict[color]))
        sds.append(np.std(bDict[color]) / np.sqrt(len(bDict[color])))
        prefs.append(pDict[color])
    orderIndices = np.argsort(prefs)
    xs = []
    ys = []
    errs = []
    for ind in orderIndices:
        xs.append(colors[ind])
        ys.append(brkTimes[ind])
        errs.append(sds[ind])
    plt.subplots()[1].set_xticklabels([''] + xs)
    plt.bar(range(6), ys, width=0.5, align='center')
    plt.errorbar(range(6), ys, yerr=errs, ecolor='black', fmt='.')
    plt.ylabel('Mean Suppression Time (s)')
    plt.xlabel('Stimulus Color (RGB255)')
    plt.title('Suppression Time By Color (Most to Least Favorite)')
    plt.savefig(outDir + 'ST' + inFile[-6:-4] + '.png', dpi=100)
    plt.close()

def plotSThist(inFile, outDir):
    '''
    Saves a line graph of the suppression time history (averaged into 6 bins) 
    from the given input file to the given output directory.
    '''
    ys = breaksHistory(inFile, True)
    plt.plot(range(6), ys)
    plt.title('Suppression Time Training Effect')
    plt.ylim(0, 10)
    plt.savefig(outDir + 'SThist' + inFile[-6:-4] + '.png', dpi=100)
    plt.close() 
    
def plotCombinedST(outDir):
    '''Saves a bar chart of the mean suppression times for each rank of preference across all subjects.'''
    data = [[], [], [], [], [], []]
    norms = []
    for id in SUBJECTS:
        inFile = '/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt'
        bDict = breaksToDict(inFile, True)
        pDict = prefsToDict(inFile, False)
        for i in range(6):
            #data[i] += bDict[pDict[i + 1]]
            data[i].append(np.mean(bDict[pDict[i + 1]]))
        norms.append((np.mean(bDict[pDict[1]]) - np.mean(bDict[pDict[6]]))/ (np.mean(bDict[pDict[1]]) + np.mean(bDict[pDict[6]])) * 2)
    errs = []
    for i in range(6):
        errs.append(np.std(data[i]) / np.sqrt(len(data[i])))
    print stats.f_oneway(data[0], data[1], data[2], data[3], data[4], data[5])
    print stats.ttest_rel(norms, np.zeros(len(norms)))
    for i, lst in enumerate(data):
        data[i] = np.mean(lst)
    plt.subplots()[1].set_xticklabels(['', '1st Fav.', '2nd Fav.', '3rd Fav.', '4th Fav.', '5th Fav.', '6th Fav.'])
    plt.bar(range(6), data, width=0.5, align='center')
    plt.errorbar(range(6), data, yerr=errs, ecolor='black', fmt='.')
    plt.ylabel('Mean Suppression Time (s)')
    plt.xlabel('Preference Ranking')
    plt.title('Suppression Time By Preference')
    plt.savefig(outDir + 'STcombined.png', dpi=100)
    plt.close()
        
def plotCombinedSTDiff(outDir):
    '''
    Saves a bar chart of the mean suppression time differences (from the mean suppression time of the favorite color)
    for each rank of preference across all subjects into the given output directory.
    '''
    data = [[], [], [], [], [], []]
    norms = []
    for id in SUBJECTS:
        inFile = '/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt'
        bDict = breaksToDict(inFile, True)
        pDict = prefsToDict(inFile, False)
        data[0].append(0)
        for i in range(1, 6):
            #data[i] += bDict[pDict[i + 1]]
            data[i].append((np.mean(bDict[pDict[i + 1]]) - np.mean(bDict[pDict[1]])) / np.mean(bDict[pDict[1]]) * 100)
        norms.append((np.mean(bDict[pDict[1]]) - np.mean(bDict[pDict[6]]))/ (np.mean(bDict[pDict[1]]) + np.mean(bDict[pDict[6]])) * 2)
    errs = []
    for i in range(1, 6):
        errs.append(np.std(data[i]) / np.sqrt(len(data[i])))
    print stats.f_oneway(data[0], data[1], data[2], data[3], data[4], data[5])
    print stats.ttest_rel(norms, np.zeros(len(norms)))
    for i, lst in enumerate(data):
        data[i] = np.mean(lst)
    plt.subplots()[1].set_xticklabels(['', '2nd Fav.', '3rd Fav.', '4th Fav.', '5th Fav.', '6th Fav.'])
    plt.bar(range(5), data[1:], width=0.5, align='center')
    plt.errorbar(range(5), data[1:], yerr=errs, ecolor='black', fmt='.')
    plt.ylabel('Mean Suppression Time Difference (%)')
    plt.xlabel('Preference Ranking')
    plt.title('Suppression Time Difference from Favorite Color')
    plt.savefig(outDir + 'STdiffCombined.png', dpi=100)
    plt.close()
    
def plotSTbyHue(outDir):
    '''Saves a bar chart of the mean suppression times for each hue across all subjects.'''
    data = [[], [], [], [], [], []]
    for id in SUBJECTS:
        tempDict = breaksToDict('/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt', True)
        for i, color in enumerate(colorlist('/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt')):
            data[i] += tempDict[color]   
    errs = []
    for i in range(6):
        errs.append(np.std(data[i]) / np.sqrt(len(data[i])))
    for i, lst in enumerate(data):
        data[i] = np.mean(lst)
    
    plt.subplots()[1].set_xticklabels(['', 'red', 'orange', 'yellow', 'green', 'blue', 'purple'])
    plt.bar(range(6), data, width=0.5, align='center')
    plt.errorbar(range(6), data, yerr=errs, ecolor='black', fmt='.')
    plt.ylabel('Mean Suppression Time (s)')
    plt.xlabel('Stimulus Hue')
    plt.title('Suppression Time By Hue')
    plt.savefig(outDir + 'STcombinedHue.png', dpi=100)
    plt.close()
    
def plotCH(inFile, outDir):
    '''
    Saves a double line graph of the calibration history of both staircases
    from the given input file to the given output directory.
    '''
    y1s, y2s = calibrationHistory(inFile)
    plt.plot(range(len(y1s)), y1s)
    plt.plot(range(len(y2s)), y2s)
    plt.title('Tilt Magnitude History During Calibration')
    plt.ylabel('Tilt Magnitude (degrees)')
    plt.xlabel('Trial # (for the staircase)')
    plt.savefig(outDir + 'calibHist' + inFile[-6:-4] + '.png', dpi=100)
    plt.close()
    
def plotOA(inFile, outDir):
    '''
    Saves a bar chart of the orientation task accuracies for the four relevant trial categories
    from the given input file to the given output directory.
    '''
    accData =  oriTaskAcc(inFile, False)
    pDict = prefsToDict(inFile, False)
    leastFavColor, favColor = pDict[6], pDict[1]
    barLabels = [leastFavColor + ' opposite', leastFavColor + ' cued', favColor + ' opposite', favColor + ' cued']
    ys = (accData['leastFavOpp'], accData['leastFavSame'], accData['favOpp'], accData['favSame'])
    barList = plt.bar(range(4), ys, align='center')
    leastFavColor, favColor = leastFavColor[1:-1].split(','), favColor[1:-1].split(',')
    for i in range(3):
        leastFavColor[i] = float(leastFavColor[i]) / 180
        favColor[i] = float(favColor[i]) / 180
    barList[0].set_color(leastFavColor)
    barList[1].set_color(leastFavColor)
    barList[2].set_color(favColor)
    barList[3].set_color(favColor)
    plt.xticks(range(4), barLabels, rotation=10)
    plt.ylabel('Proportion of Correct Responses')
    plt.title('Orientation Task Accuracy with Unconscious Cueing')
    plt.savefig(outDir + 'OA' + inFile[-6:-4] + '.png', dpi=100)
    plt.close()
  
def plotCombinedOA(validSubjects, outDir):
    '''
    Saves a bar chart of the orientation task accuracies for the four relevant trial categories
    across the given subjects to the given output directory.
    '''
    ys = np.zeros((4, 1))
    favCueEffect = []
    leastFavCueEffect = []
    for id in validSubjects:
        accData = oriTaskAcc('/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt', False)
        orderedData = (accData['leastFavOpp'], accData['leastFavSame'], accData['favOpp'], accData['favSame'])
        favCueEffect.append((accData['favOpp'] - accData['favSame']) / (accData['favOpp'] + accData['favSame']) * 2)
        leastFavCueEffect.append((accData['leastFavOpp'] - accData['leastFavSame']) / (accData['leastFavOpp'] + accData['leastFavSame']) * 2)
        for i in range(4):
            ys[i] += orderedData[i] / len(validSubjects)
    print 'Fav: ' + str(np.mean(favCueEffect))
    print 'leastFav: ' + str(np.mean(leastFavCueEffect))
    prefEffect = np.array(favCueEffect) - np.array(leastFavCueEffect)
    plt.bar(range(len(favCueEffect)), favCueEffect)
    plt.close()
    print ys
    print stats.ttest_rel(favCueEffect, np.zeros(len(favCueEffect)))
    print stats.ttest_rel(leastFavCueEffect , np.zeros(len(leastFavCueEffect)))
    print stats.ttest_rel(prefEffect , np.zeros(len(prefEffect)))
    barLabels = ('Least Fav. Distract', 'Least Fav. Cue', 'Fav. Distract', 'Fav. Cue')
    barList = plt.bar(range(4), ys, align='center')
    plt.xticks(range(4), barLabels, rotation=10)
    plt.ylim(0.5, 1.0)
    plt.ylabel('Proportion of Correct Responses')
    plt.title('Orientation Task Accuracy with Unconscious Cueing')
    plt.savefig(outDir + 'OAcombined.png', dpi=100)
    plt.close()
    
def plotCombinedOS(validSubjects, outDir):
    '''
    Saves a bar chart of the orientation task reaction times for the four relevant trial categories
    across the given subjects to the given output directory.
    '''
    ys = np.zeros((4, 1))
    favCueEffect = []
    leastFavCueEffect = []
    for id in validSubjects:
        accData = oriTaskSpd('/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt')
        orderedData = (accData['leastFavOpp'], accData['leastFavSame'], accData['favOpp'], accData['favSame'])
        favCueEffect.append((accData['favOpp'] - accData['favSame']) / (accData['favOpp'] + accData['favSame']) * 2)
        leastFavCueEffect.append((accData['leastFavOpp'] - accData['leastFavSame']) / (accData['leastFavOpp'] + accData['leastFavSame']) * 2)
        for i in range(4):
            ys[i] += orderedData[i] / len(validSubjects)
    print 'Fav: ' + str(np.mean(favCueEffect))
    print 'leastFav: ' + str(np.mean(leastFavCueEffect))
    print ys
    prefEffect = np.array(favCueEffect) - np.array(leastFavCueEffect)
    print stats.ttest_rel(favCueEffect, np.zeros(len(favCueEffect)))
    print stats.ttest_rel(leastFavCueEffect , np.zeros(len(leastFavCueEffect)))
    print stats.ttest_rel(prefEffect , np.zeros(len(prefEffect)))
    barLabels = ('Least Fav. Distract', 'Least Fav. Cue', 'Fav. Distract', 'Fav. Cue')
    barList = plt.bar(range(4), ys, align='center')
    plt.xticks(range(4), barLabels, rotation=10)
    plt.ylabel('Proportion of Correct Responses')
    plt.title('Orientation Task Speed with Unconscious Cueing')
    plt.savefig(outDir + 'OScombined.png', dpi=100)
    plt.close()

def plotEffectCorr(validSubjects, outDir):
    xs, ys = [], []
    for id in validSubjects:
        if id in SUBJECTS:
            inFile = '/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt'
            bDict = breaksToDict(inFile, True)
            pDict = prefsToDict(inFile, False)
            favNormST, leastFavNormST = np.mean(bDict[pDict[1]]), np.mean(bDict[pDict[6]])
            xs.append((favNormST - leastFavNormST) / (favNormST + leastFavNormST) * 2)
            accData = oriTaskSpd(inFile)
            ys.append((accData['favOpp'] - accData['favSame']) / (accData['favOpp'] + accData['favSame']) * 2 -             
                      (accData['leastFavOpp'] - accData['leastFavSame']) / (accData['leastFavOpp'] + accData['leastFavSame']) * 2)                
    plt.scatter(xs, ys)
    s, intercept, Rval, pval, stdErr = stats.linregress(xs, ys)
    plt.text(-0.15, .15, 'R = ' + str(Rval) + '\np = ' + str(pval))
    plt.xlabel('Preference Effect on Suppression Time (Normalized)')
    plt.ylabel('Preference Effect on Cue Strength (Normalized)')
    plt.title('Experiment 1 vs. Experiment 2 Effect Strength')
    plt.savefig(outDir + 'ECspeed.png', dpi=100)
    plt.close()
    
def accOutliers(validSubjects, stdevs):
    accs = {'favSame':[], 'favOpp':[], 'leastFavSame':[], 'leastFavOpp':[]}
    avgAccs = []
    output = []
    for id in validSubjects:
        accData = oriTaskSpd('/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt')
        for cond in accs.keys():
            accs[cond].append(accData[cond])
        avgAccs.append(np.mean(accData.values()))
    for cond in accs.keys():
        lower = np.mean(accs[cond]) - stdevs * np.std(accs[cond])
        upper = np.mean(accs[cond]) + stdevs * np.std(accs[cond])
        for i in range(len(accs[cond]) - 1, -1, -1):
            if accs[cond][i] < lower or accs[cond][i] > upper and validSubjects[i] not in output:
                output.append(validSubjects[i])
    lower = np.mean(avgAccs) - stdevs * np.std(avgAccs)
    upper = np.mean(avgAccs) + stdevs * np.std(avgAccs)
    for i in range(len(avgAccs) - 1, -1, -1):
        if avgAccs[i] < lower or avgAccs[i] > upper and validSubjects[i] not in output:
            output.append(validSubjects[i])
    return output
    
if __name__ == '__main__':
    inFile = '/home/shimojolab/PsychopyExperiments/colorPrefData/expData27.txt'
    outDir = '/home/shimojolab/PsychopyExperiments/colorPrefFigures/'
    plotST(inFile, outDir)
    plotOA(inFile, outDir)
    plotCH(inFile, outDir)

    plotCombinedSTDiff(outDir)
    for id in SUBJECTS:
        inFile = '/home/shimojolab/PsychopyExperiments/colorPrefData/expData' + id + '.txt'
        #plotST(inFile, outDir)
        #plotSThist(inFile, outDir)
    #plotSTbyHue(outDir)
    # 4, 16, 18, 26
    validSubjects = ['01', '02', '04', '06', '10', '12', '16', '18', '20', '21', '22', '23', '25', '26', '27']  # those with satisfactory calibration
    #plotCombinedOA(validSubjects, outDir)
    #plotCombinedOS(validSubjects, outDir)
    #plotEffectCorr(validSubjects, outDir)
    #print accOutliers(validSubjects, 3)
        

        
        
    
