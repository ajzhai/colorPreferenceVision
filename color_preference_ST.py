from psychopy import visual, core, event
import singleColorCross as crss
import numpy as np
import random
import time

'''
TODO: how to make sure least-favorite blue can get in equiluminance range of most-favorite yellow?
'''

PATH_TO_MONDRIANS = 'Mondrians/newColors/'
PATH_TO_STIMULI = 'ColorStimuli/'
OUTPUT_FILE = open('colorPrefData/test1.txt', 'a')
CENTER_DIST = 0.5  # positive for right-eye dominant, negative for left-eye dominant
YPOS = 0.1
TEXT_SIZE = 0.038
REFRESH_RATE = 60  # in Hz
FIRST_STAGE_REPETITIONS = 0 # per color
SECOND_STAGE_REPETITIONS = 1  # per layout 
colorsToTest = [(128, 0, 0), (128, 64, 0), (128, 128, 0),
                (0, 128, 0), (0, 0, 128), (128, 0, 128)]
                
# All possible trial configurations for second experiment
layouts = []
for popColor in [1, 2]:
    for popLoc in [-0.128, 0.128]:
        for gabLoc in [-0.128, 0.128]:
            for gabTilt in [-30, 30]:
                layouts.append((popColor, popLoc, gabLoc, gabTilt))
                    
# Global Initialization
win = visual.Window((1920, 1080), fullscr=True, allowGUI=False, 
                     monitor="shimojoLab", color='black')
ASPECT_RATIO = float(win.size[0]) / win.size[1]

# Background                      
leftFix = visual.Circle(win, lineColor='white', fillColor='white', 
                        size=(0.0045, 0.0045 * ASPECT_RATIO), pos=(-CENTER_DIST, YPOS))
rightFix = visual.Circle(win, lineColor='white', fillColor='white', 
                         size=(0.0045, 0.0045 * ASPECT_RATIO), pos=(CENTER_DIST, YPOS))
leftBox = visual.Rect(win, lineColor='white', fillColor='black', 
                      size=(0.54, 0.54 * ASPECT_RATIO), pos=(-CENTER_DIST, YPOS))
rightBox = visual.Rect(win, lineColor='white', fillColor='black', 
                       size=(0.54, 0.54 * ASPECT_RATIO), pos=(CENTER_DIST, YPOS))

# Instructions
instructL1 = visual.TextStim(win, pos=(-CENTER_DIST, 0.14 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                             text='Hit space when ready.')
instructL2 = visual.TextStim(win, pos=(-CENTER_DIST, -0.12 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                             text='Then, press space again when you see a colored dot.')
instructR1 = visual.TextStim(win, pos=(CENTER_DIST, 0.14 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                             text='Hit space when ready.')
instructR2 = visual.TextStim(win, pos=(CENTER_DIST, -0.12 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                             text='Then, press space again when you see a colored dot.')

# Mondrians and Suppressed Stimulus
mond1 = visual.ImageStim(win, size=(0.08, 0.0675 * ASPECT_RATIO), pos=(CENTER_DIST, YPOS),
                         image=PATH_TO_MONDRIANS + '01.jpg')
mond2 = visual.ImageStim(win, size=(0.08, 0.0675 * ASPECT_RATIO), pos=(CENTER_DIST, YPOS),
                         image=PATH_TO_MONDRIANS + '01.jpg')
stim = visual.ImageStim(win, size=(0.045, 0.045 * ASPECT_RATIO), pos=(-CENTER_DIST, YPOS), 
                        image=PATH_TO_STIMULI + str(colorsToTest[0]) + '.png')
                        
# Suppressed Priming Ring of Crosses
ringXY = []
for ang in np.arange(0.75, 2.75, .25):
    ringXY.append((0.072 * np.cos(ang * np.pi), 0.128 * np.sin(ang * np.pi)))
primingRing = visual.ElementArrayStim(win, fieldPos=(-CENTER_DIST, YPOS), sizes=(0.018, 0.018 * ASPECT_RATIO), 
                                      nElements=8, xys=ringXY, elementMask=None, 
                                      elementTex=PATH_TO_STIMULI + str(colorsToTest[0]) + '.png')
                                      
# Orientation Task Gabor
tex1 = np.zeros((256, 256, 3))
tex2 = np.zeros((256, 256, 3))
for y in range(256):
    hCenter = 128 + np.arctan(np.pi / 6) * (y - 128)  # gabor is rotated by 30 degrees
    for x in range(256):
        val1 = np.sin((x - hCenter) * 2.0 * np.pi / 256 * 6)  # spatial frequency (sine periods)      
        val2 = np.sin((x + hCenter) * 2.0 * np.pi / 256 * 6)
        tex1[y][x] = (val1, val1, val1)
        tex2[y][x] = (val2, val2, val2)
gabor = visual.GratingStim(win, mask="gauss", size=[0.045, 0.045 * ASPECT_RATIO])
                                      
# Location Task Text
questionL = visual.TextStim(win, pos=(-CENTER_DIST, 0.14 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                            text='Location?')
choicesL = visual.TextStim(win, pos=(-CENTER_DIST, YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                           text='Left (L)       Right (R)')
questionR = visual.TextStim(win, pos=(CENTER_DIST, 0.14 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                            text='Location?')
choicesR = visual.TextStim(win, pos=(CENTER_DIST, YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                           text='Left (L)       Right (R)')

# Confirmation Text
confL = visual.TextStim(win, height=TEXT_SIZE, wrapWidth=0.23, 
                        text='Response received!', pos=(-CENTER_DIST, 0.1 + YPOS))
confR = visual.TextStim(win, height=TEXT_SIZE, wrapWidth=0.23, 
                        text='Response received!', pos=(CENTER_DIST, 0.1 + YPOS))

# Graphics for Preference Ranking and Flicker Photometry
circles = {}
ranks = {}
for i, color in enumerate(colorsToTest):
    hPos = (i - (len(colorsToTest) - 1) / 2.0) * 0.1
    circles[color] = visual.ImageStim(win, size=(0.045, 0.045 * ASPECT_RATIO), pos=(hPos, 0.2),
                                      image=PATH_TO_STIMULI + str(color) + '.png')
    ranks[color] = visual.TextStim(win, height=TEXT_SIZE, pos=(hPos, 0.12), text='_')
indicator = visual.Rect(win, lineColor='white', fillColor='black', size=(0.12, 0.225 * ASPECT_RATIO), 
                           pos=(-(len(colorsToTest) - 1) / 2.0 * 0.1, 0.175))
instructions = visual.TextStim(win, pos=(0, 0.4), height=TEXT_SIZE, wrapWidth = 0.8,
                               text='Enter your preference ranking (1 for most favorite, 6 for least ' + \
                                    'favorite) for the indicated color. Press x to clear all if you ' + \
                                    'make a mistake. The experiment will continue once all 6 colors have been ranked.')
flickerer = visual.Circle(win, pos=(0, 0.1), size=(0.18, 0.18 * ASPECT_RATIO), 
                          fillColorSpace='rgb255', lineColorSpace='rgb255')
sliderBar = visual.Line(win, start=(-0.3, -0.2), end=(0.3, -0.2), lineColor='gray')
                                    
# Ending Message
endMsgL = visual.TextStim(win, height=TEXT_SIZE, wrapWidth=0.23, pos=(-CENTER_DIST, 0.12 + YPOS),
                          text='All trials have been completed. Thank you for your participation!')
endMsgR = visual.TextStim(win, height=TEXT_SIZE, wrapWidth=0.23, pos=(CENTER_DIST, 0.12 + YPOS),
                          text='All trials have been completed. Thank you for your participation!')
endMsg = visual.TextStim(win, height=TEXT_SIZE, wrapWidth=0.8, pos=(0, 0),
                         text='All trials have been completed. Thank you for your participation!')
                           
def cleanExit():
    '''Properly exits the experiment.'''
    OUTPUT_FILE.close()
    win.close()
    core.quit()

def drawBackground():
    '''Draws the boxes and the fixation points for each eye's view .'''
    leftBox.draw()
    leftFix.draw()
    rightBox.draw()
    rightFix.draw()

def showConfirmation():
    '''Displays a message confirming reception of response for 1 second.'''
    for frameN in range(REFRESH_RATE):
        drawBackground()
        confL.draw()
        confR.draw()
        win.flip()
        
def waitForReady(isSecondStage):
    '''Draws instructions for the subject and waits for the subject to press a key.'''
    drawBackground()
    if isSecondStage:
        instructL2.text = 'When you see a striped pattern, press the arrow key in the direction of tilt.'
        instructR2.text = 'When you see a striped pattern, press the arrow key in the direction of tilt.'
    instructL1.draw()
    instructL2.draw()
    instructR1.draw()
    instructR2.draw()
    win.flip()  
    # pause until there's a keypress
    input = event.waitKeys(keyList=['space', 'escape'])
    if input[0] == 'escape':
        cleanExit()

def askForLocation(loc):
    '''Draws the question for the location task and waits for subject to answer.'''
    drawBackground()
    questionL.draw()
    choicesL.draw()
    questionR.draw()
    choicesR.draw()
    win.flip()  
    answer = event.waitKeys(keyList=['left', 'right'])
    return (answer[0] == 'left' and loc < 0) or (answer[0] == 'right' and loc > 0)    
    
def circleBreakingTime(color, askLocation, blinking):
    '''
    Runs a full trial of measuring the breaking time for a suppressed circle 
    stimulus of the given color. Writes results to output text file.
    '''
    loc = (np.random.randint(0, 2) - 0.5) / 8 # relative to center of box
    mond1.pos =  (CENTER_DIST + loc, YPOS)
    mond2.pos = (CENTER_DIST - loc, YPOS)
    stim.image = PATH_TO_STIMULI + str(color) + '.png'
    stim.pos = (-CENTER_DIST + loc, YPOS)
    waitForReady(False)
    fixTime = np.random.randint(0, REFRESH_RATE)
    for frameN in range(fixTime):
        drawBackground()
        win.flip()
    mondN = 0
    startTime = time.time()
    for frameN in range(int(10.8 * REFRESH_RATE)):  # want to allow up to 10 seconds, last display is for finding bad subjects 
        drawBackground()
        if int(frameN % (REFRESH_RATE / 10.0)) == 0:  # change mondrian 10 times per second
            mondN += 1
            if mondN > 9:  # there are 10 mondrians to cycle through
                mondN = 0
            mond1.image = PATH_TO_MONDRIANS + '0' + str(mondN) + '.jpg'
            mond2.image = PATH_TO_MONDRIANS + '0' + str(mondN) + '.jpg'            
        if blinking:
            if frameN % int(REFRESH_RATE * 0.6) < REFRESH_RATE / 3.0 + 4:
                if frameN < 10 * REFRESH_RATE:
                    mond1.draw()
                    mond2.draw()
                if frameN % int(REFRESH_RATE * 0.6) >= 2 and frameN % int(REFRESH_RATE * 0.6) < REFRESH_RATE / 3.0 + 2:
                    stim.draw()
        else:
            stim.draw()
            if frameN < 10 * REFRESH_RATE:
                mond1.draw()
                mond2.draw()
        if event.getKeys(keyList=['space']):
            breakingTime = time.time() - startTime
            win.flip()
            if askLocation:
                passedTask = askForLocation(loc)
            print str(color) + ': ' + str(breakingTime) + ' seconds, test passed=' + str(passedTask)
            OUTPUT_FILE.write(str(color).replace(' ', '') 
                               + ' ' + str(breakingTime) 
                               + ' ' + str(passedTask) + '\n')
            break
        win.flip()
    event.clearEvents()   
    showConfirmation()

def recordPreference(colors):
    '''
    Records subject's preference ranking for each color and writes to a text file. 
    Returns tuple of (most favorite color, least favorite color).
    '''
    indicator.autoDraw = True
    for color in colorsToTest:
        circles[color].autoDraw = True
        ranks[color].autoDraw = True   
    instructions.autoDraw = True
    unusedRanks = []
    for i in range(1, len(colorsToTest) + 1):
        unusedRanks.append(str(i))
    for color in colorsToTest:
        indicator.pos = (circles[color].pos[0], 0.175)
        win.flip()
        input = event.waitKeys(keyList=unusedRanks + ['x'])
        if input[0] == 'x':
            event.clearEvents()
            for color in colorsToTest:
                #  erase all the rankings
                ranks[color].text = '_'
            recordPreference(colors)
            break
        else:
            ranks[color].text = input[0]
            unusedRanks.remove(input[0])       
    if len(unusedRanks) == 0:
        for color in colorsToTest:
            OUTPUT_FILE.write(str(color).replace(' ', '') + str(ranks[color].text) + ' ')
        OUTPUT_FILE.write('\n\n')
    event.clearEvents()
    indicator.autoDraw = False
    for color in colorsToTest:
        circles[color].autoDraw = False
        ranks[color].autoDraw = False
        if ranks[color].text == '6':
            leastFav = color
        elif ranks[color].text == '1':
            mostFav = color
    return (mostFav, leastFav)
    
    
def equiluminance(color1, color2):
    '''Employs heterochromatic flicker photometry to return equiluminant colors of given hues.'''
    flickerer.autoDraw = True
    sliderBar.autoDraw = True
    #  Reusing the indicator object
    indicator.pos = (0, -0.2)
    indicator.size = (0.01, 0.02 * ASPECT_RATIO)
    indicator.autoDraw = True
    instructions.text = 'Press the left and right arrow keys to adjust the luminance of the colors. When' + \
                        ' the circle does not seem to flicker anymore, press space to continue.'
    scaleFactor = 1.0
    temp2 = (int(color2[0] * scaleFactor), int(color2[1] * scaleFactor), int(color2[2] * scaleFactor))
    while not event.getKeys(keyList=['space']):
        flickerer.fillColor = color1
        flickerer.lineColor = color1
        for frameN in range(REFRESH_RATE / 30):  # show each color for 1/30th of a second
            win.flip()
        flickerer.fillColor = temp2
        flickerer.lineColor = temp2
        for frameN in range(REFRESH_RATE / 30):
            win.flip()
        input = event.getKeys(keyList=['left', 'right'])
        if input and input[0] == 'left':
            if scaleFactor > 0.04:
                scaleFactor -= 0.04
                indicator.pos = ((scaleFactor - 1.0) * 0.3, -0.2)
            temp2 = (int(color2[0] * scaleFactor), int(color2[1] * scaleFactor), int(color2[2] * scaleFactor))
        elif input and input[0] == 'right':
            if scaleFactor < 1.96:
                scaleFactor += 0.04
                indicator.pos = ((scaleFactor - 1.0) * 0.3, -0.2)
            temp2 = (int(color2[0] * scaleFactor), int(color2[1] * scaleFactor), int(color2[2] * scaleFactor))
    event.clearEvents()
    instructions.autoDraw = False
    flickerer.autoDraw = False
    sliderBar.autoDraw = False
    indicator.autoDraw = False
    return (color1, temp2)
    
def ringPrime(stimColor, ringColor, popLoc):
    '''
    Presents a suppressed ring of 8 cross-circles as a prime. The top cross-circle is of a different color.
    Returns whether or not the subject indicated (by pressing space) that they saw the ring. 
    '''
    mond1.size = (0.2, 0.4)
    mond1.pos = (CENTER_DIST, YPOS)
    stim.size = (0.018, 0.018 * ASPECT_RATIO)  # reusing same stim object from first experiment
    stim.pos = (-CENTER_DIST, YPOS + popLoc)
    stim.image = PATH_TO_STIMULI + str(stimColor) + '.png'
    primingRing.elementTex = PATH_TO_STIMULI + str(ringColor) + '.png'
    mondN = 0
    for frameN in range(REFRESH_RATE):
        if int(frameN % (REFRESH_RATE / 10.0)) == 0:  # change mondrian 10 times per second
            mondN += 1
            if mondN > 9:  # there are 10 mondrians to cycle through
                mondN = 0
            mond1.image = PATH_TO_MONDRIANS + '0' + str(mondN) + '.jpg'
        drawBackground()
        primingRing.draw()
        mond1.draw()
        stim.draw()
        if event.getKeys(keyList=['space']):
            event.clearEvents()
            return True
        win.flip()
    return False

def askVisible():
    '''CURRENTLY UNUSED: Draws the question asking whether the subject saw the prime and waits for subject to answer.'''
    event.clearEvents()
    drawBackground()
    questionL.text = 'Did you see a ring of circles?'
    choicesL.text = 'Yes (L)       No (R)'
    questionR.text = 'Did you see a ring of circles?'
    choicesR.text = 'Yes (L)       No (R)'
    questionL.draw()
    choicesL.draw()
    questionR.draw()
    choicesR.draw()
    win.flip()  
    answer = event.waitKeys(keyList=['left', 'right'])
    return answer[0] == 'left'
    
def orientationTask(color1, color2, layout):  
    '''
    Runs a full trial of measuring the speed of performing an orientation task
    after a pop-out prime of the given colors at the location determined by
    the given layout tuple. Writes results to output text file.
    
    Layout tuple format: 
    (color of the popout cross, location (top or bottom) of popout, location of gabor, clockwise tilt of gabor)
    '''
    waitForReady(True)
    if layout[0] == 1:
        primeVisible = ringPrime(color1, color2, layout[1])
    else:
        primeVisible = ringPrime(color2, color1, layout[1])
    if primeVisible:
        #OUTPUT_FILE.write(str(layout) + ' ' + str(askColor()) + '\n')
        pass
    else:
        gabor.pos = (-CENTER_DIST, YPOS + layout[2])
        if layout[3] > 0:
            gabor.tex = tex1
        else:
            gabor.tex = tex2
        drawBackground()
        gabor.draw()
        startTime = time.time()
        win.flip()
        answer = event.waitKeys(keyList=['left', 'right'])
        responseTime = time.time() - startTime
        passedTask = (answer[0] == 'left' and layout[3] < 0) or (answer[0] == 'right' and layout[3] > 0)  
        OUTPUT_FILE.write(str(layout) + ' ' + str(responseTime) + ' ' + str(passedTask) + '\n')
        event.clearEvents()
    showConfirmation()
    
def showEndMsg():
    '''Displays message signifying the end of the experiment and waits for quit.'''
    endMsg.draw()
    win.flip()
    event.waitKeys(keyList=['q'])
    
    
if __name__ == '__main__':
    print win.size
    print win.getActualFrameRate()
    trialOrder = []
    for i in range(len(colorsToTest)):
        trialOrder += [i] * FIRST_STAGE_REPETITIONS
    np.random.shuffle(trialOrder)
    for trialColor in trialOrder:
        circleBreakingTime(colorsToTest[trialColor], True, True)
    extremes = recordPreference(colorsToTest)
    newColors = equiluminance(extremes[0], extremes[1])
    crss.makeCross(newColors[0])    
    crss.makeCross(newColors[1])
    trialOrder = []
    for i in range(len(layouts)):
        trialOrder += [i] * SECOND_STAGE_REPETITIONS
    np.random.shuffle(trialOrder)
    for layoutN in trialOrder:
        orientationTask(newColors[0], newColors[1], layouts[layoutN])
    showEndMsg()
    
# Global cleanup
cleanExit()