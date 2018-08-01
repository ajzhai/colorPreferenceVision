from psychopy import visual, core, event
import singleColorCross as crss
import numpy as np
import random
import time

'''
TODO: ask about ring dimensions
'''

PATH_TO_MONDRIANS = 'Mondrians/newColors/'
PATH_TO_STIMULI = 'ColorStimuli/'
OUTPUT_FILE = open('colorPrefData/testAug1.txt', 'a')
CENTER_DIST = 0.4  # positive for right-eye dominant, negative for left-eye dominant
YPOS = 0.1
LEFT_SHIFT = 0.055
TEXT_SIZE = 0.038
REFRESH_RATE = 60  # in Hz
FIRST_STAGE_REPETITIONS = 0 # per color + side combination
SECOND_STAGE_REPETITIONS = 5  # per layout 

colorsToTest = [(27, 0, 0), (12, 6, 0), (8, 8, 0), (0, 10, 0), (0, 0, 120), (24, 0, 24)]
tweak = 0.3
for i, color in enumerate(colorsToTest):
    colorsToTest[i] = (int(round(color[0] * tweak)), int(round(color[1] * tweak)), int(round(color[2] * tweak)))
                
                    
# Global Initialization
win = visual.Window((1920, 1080), fullscr=True, allowGUI=False, 
                     monitor="shimojoLab", color='black')
ASPECT_RATIO = float(win.size[0]) / win.size[1]

# Background                      
leftFix1 = visual.Rect(win, lineColor='white', fillColor='white', size=(0, 0.029 * ASPECT_RATIO), pos= (-CENTER_DIST, YPOS + LEFT_SHIFT))
leftFix2 = visual.Rect(win, lineColor='white',fillColor='white', size=(0.03, 0 * ASPECT_RATIO), pos= (-CENTER_DIST, YPOS + LEFT_SHIFT))
rightFix1 = visual.Rect(win, lineColor='white',fillColor='white', size=(0.03, 0 * ASPECT_RATIO), pos= (CENTER_DIST, YPOS))
rightFix2 = visual.Rect(win, lineColor='white',fillColor='white', size=(0, 0.03 * ASPECT_RATIO), pos= (CENTER_DIST, YPOS))
rightFixBorder = visual.Circle(win, lineColor='black', fillColor='black',
                               size=(0.018, 0.018 * ASPECT_RATIO), pos=(CENTER_DIST, YPOS))
lattice = np.zeros((256, 256))
for y in range(256):
     if y % 28 >= 14: 
         for x in range(256):
            lattice[y][x] = 1
for x in range(256):
     if x % 28 >= 14: 
         for y in range(256):
            lattice[y][x] = 1
sqrOutline = np.ones((256, 256))
for y in range(3, 253):
    for x in range(3, 253):
        sqrOutline[y][x] = -1
leftBox = visual.GratingStim(win, color='white', tex=lattice, mask=sqrOutline,
                             size=(0.27, 0.27 * ASPECT_RATIO), pos=(-CENTER_DIST, YPOS + LEFT_SHIFT))
#rightBox = visual.Rect(win, lineColor='white', fillColor='black', 
 #                      size=(0.54, 0.54 * ASPECT_RATIO), pos=(CENTER_DIST, YPOS))
rightBox = visual.GratingStim(win, color='white', tex=lattice, mask=sqrOutline,
                              size=(0.27, 0.27 * ASPECT_RATIO), pos=(CENTER_DIST, YPOS))

# Instructions
instructL1 = visual.TextStim(win, pos=(-CENTER_DIST, 0.14 + YPOS + LEFT_SHIFT), height=TEXT_SIZE, wrapWidth=0.23,
                             text='Hit space when ready.')
instructL2 = visual.TextStim(win, pos=(-CENTER_DIST, -0.12 + YPOS + LEFT_SHIFT), height=TEXT_SIZE, wrapWidth=0.23,
                             text='Then, press space again when you see a colored dot.')
instructR1 = visual.TextStim(win, pos=(CENTER_DIST, 0.14 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                             text='Hit space when ready.')
instructR2 = visual.TextStim(win, pos=(CENTER_DIST, -0.12 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                             text='Then, press space again when you see a colored dot.')

# Mondrians and Suppressed Stimulus
monds1 = []
monds2 = []
for i in range(10):
    monds1.append(visual.ImageStim(win, size=(0.08, 0.08 * ASPECT_RATIO), pos=(CENTER_DIST + 0.5 / 8, YPOS),
                                   image=PATH_TO_MONDRIANS + 'circ0' + str(i) + '.jpg'))
    monds2.append(visual.ImageStim(win, size=(0.08, 0.08 * ASPECT_RATIO), pos=(CENTER_DIST - 0.5 / 8, YPOS),
                                   image=PATH_TO_MONDRIANS + 'circ0' + str(i) + '.jpg'))
stim = visual.GratingStim(win, size=(0.018, 0.018 * ASPECT_RATIO), 
                          colorSpace='rgb255', tex=None, mask=crss.msk)
                       
# Suppressed Priming Ring of Crosses
ringXY = []
ringRadius = 0.12  # vertical
for ang in np.arange(0.75, 2.75, .25):
    ringXY.append((ringRadius / ASPECT_RATIO * np.cos(ang * np.pi), ringRadius * np.sin(ang * np.pi)))
primingRing = visual.ElementArrayStim(win, fieldPos=(-CENTER_DIST, YPOS + LEFT_SHIFT), sizes=(0.018, 0.018 * ASPECT_RATIO), 
                                      nElements=8, xys=ringXY, elementMask=crss.msk, elementTex=None, colorSpace='rgb255')
                                      
# Orientation Task Gabor
gabor = visual.GratingStim(win, mask="gauss", size=[0.024, 0.024 * ASPECT_RATIO], pos=(-CENTER_DIST, 0.12 + YPOS + LEFT_SHIFT))
                                      
# Location Task Text
questionL = visual.TextStim(win, pos=(-CENTER_DIST, 0.14 + YPOS + LEFT_SHIFT), height=TEXT_SIZE, wrapWidth=0.23,
                            text='Location?')
choicesL = visual.TextStim(win, pos=(-CENTER_DIST, YPOS + LEFT_SHIFT), height=TEXT_SIZE, wrapWidth=0.23,
                           text='Left (L)       Right (R)')
questionR = visual.TextStim(win, pos=(CENTER_DIST, 0.14 + YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                            text='Location?')
choicesR = visual.TextStim(win, pos=(CENTER_DIST, YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                           text='Left (L)       Right (R)')

# Ring Visibility Graphics
optionsL = visual.TextStim(win, pos=(-CENTER_DIST, YPOS + LEFT_SHIFT), height=TEXT_SIZE, wrapWidth=0.23,
                           text='\n\n\n\n1. Not visible  \n2. Slightly visible  \n3. Clearly visible ')
optionsR = visual.TextStim(win, pos=(CENTER_DIST, YPOS), height=TEXT_SIZE, wrapWidth=0.23,
                           text='\n\n\n\n1. Not visible  \n2. Slightly visible  \n3. Clearly visible ')
indicatorL = visual.Rect(win, lineColor='white', fillColor='black', size=(0.4, 0.05 * ASPECT_RATIO))
indicatorR = visual.Rect(win, lineColor='white', fillColor='black', size=(0.4, 0.05 * ASPECT_RATIO))
stimL1 = visual.GratingStim(win, size=(0.018, 0.018 * ASPECT_RATIO), pos=(-CENTER_DIST - 0.068, YPOS + LEFT_SHIFT),
                            colorSpace='rgb255', tex=None, mask=crss.msk)
stimL2 = visual.GratingStim(win, size=(0.018, 0.018 * ASPECT_RATIO), pos=(-CENTER_DIST + 0.068, YPOS + LEFT_SHIFT),
                            colorSpace='rgb255', tex=None, mask=crss.msk)
stimR1 = visual.GratingStim(win, size=(0.018, 0.018 * ASPECT_RATIO), pos=(CENTER_DIST - 0.068, YPOS),
                            colorSpace='rgb255', tex=None, mask=crss.msk)
stimR2 = visual.GratingStim(win, size=(0.018, 0.018 * ASPECT_RATIO), pos=(CENTER_DIST + 0.068, YPOS),
                            colorSpace='rgb255', tex=None, mask=crss.msk)
upperHalfL = visual.GratingStim(win, size=(0.24, 0.12 * ASPECT_RATIO), pos=(-CENTER_DIST, 0.11 + YPOS + LEFT_SHIFT), 
                                color='darkturquoise', tex=None, mask='gauss')
lowerHalfL = visual.GratingStim(win, size=(0.24, 0.12 * ASPECT_RATIO), pos=(-CENTER_DIST, -0.11 + YPOS + LEFT_SHIFT), 
                                color='darkturquoise', tex=None, mask='gauss')
upperHalfR = visual.GratingStim(win, size=(0.24, 0.12 * ASPECT_RATIO), pos=(CENTER_DIST, 0.11 + YPOS), 
                                color='darkturquoise', tex=None, mask='gauss')
lowerHalfR = visual.GratingStim(win, size=(0.24, 0.12 * ASPECT_RATIO), pos=(CENTER_DIST, -0.11 + YPOS), 
                                color='darkturquoise', tex=None, mask='gauss')

# Confirmation Text
confL = visual.TextStim(win, height=TEXT_SIZE, wrapWidth=0.23, 
                        text='Response received!', pos=(-CENTER_DIST, 0.1 + YPOS + LEFT_SHIFT))
confR = visual.TextStim(win, height=TEXT_SIZE, wrapWidth=0.23, 
                        text='Response received!', pos=(CENTER_DIST, 0.1 + YPOS))

# Graphics for Preference Ranking and Flicker Photometry
circles = {}
ranks = {}
for i, color in enumerate(colorsToTest):
    hPos = (i - (len(colorsToTest) - 1) / 2.0) * 0.1
    circles[color] = visual.GratingStim(win, size=(0.018, 0.018 * ASPECT_RATIO), pos=(hPos, 0.2),
                                        colorSpace='rgb255', color=color, tex=None, mask=crss.msk)
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

# Minimum Motion
msk1 = np.ones((256, 256))
msk2 = np.ones((256, 256))
segments = 8
for y in range(256):
    for x in range(256):
        if x % (256 / segments) < (64 / segments) or x % (256 / segments) >= (192 / segments):
            msk1[y][x] = -1
        if x % (256 / segments) < (128 / segments): 
            msk2[y][x] = -1
motionGrating1 = visual.GratingStim(win, pos=(0, 0.1), size=(0.6, 0.1 * ASPECT_RATIO),
                                    mask=msk1, tex=None, colorSpace='rgb255')
motionGrating2 = visual.GratingStim(win, pos=(0, 0.1), size=(0.6, 0.1 * ASPECT_RATIO),
                                    mask=-msk1, tex=None, colorSpace='rgb255')
                                   
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
    leftFix1.draw()
    leftFix2.draw()
    rightBox.draw()
    rightFix1.draw()
    rightFix2.draw()

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

def askForLocation(loc, isSecondStage):
    '''Draws the question for the location task and waits for subject to answer.'''
    drawBackground()
    choicesL.text = 'Left (L)       Right (R)'
    choicesR.text = 'Left (L)       Right (R)'
    if isSecondStage:
        questionL.text = 'Direction of tilt?'
        questionR.text = 'Direction of tilt?'
    questionL.draw()
    choicesL.draw()
    questionR.draw()
    choicesR.draw()
    win.flip()  
    answer = event.waitKeys(keyList=['left', 'right'])
    return (answer[0] == 'left' and loc < 0) or (answer[0] == 'right' and loc > 0)    
    
def circleBreakingTime(color, stimLoc, askLocation, blinking):
    '''
    Runs a full trial of measuring the breaking time for a suppressed circle 
    stimulus of the given color at the given horizontal location (relative to
    center of box). Writes results to output text file.
    '''
    stim.color = color
    stim.pos = (-CENTER_DIST + stimLoc, YPOS + LEFT_SHIFT)
    waitForReady(False)
    fixTime = np.random.randint(0, REFRESH_RATE)
    for frameN in range(fixTime):
        drawBackground()
        win.flip()
    mondN = 0
    breakingTime = 99999
    startTime = time.time()
    for frameN in range(int(10.8 * REFRESH_RATE)):  # want to allow up to 10 seconds, last display is for finding bad subjects
        if frameN <= 6 * REFRESH_RATE:
            stim.opacity = frameN / (6.0 * REFRESH_RATE)
        drawBackground()
        if int(frameN % (REFRESH_RATE / 10.0)) == 0:  # change mondrian 10 times per second
            mondN += 1
            if mondN > 9:  # there are 10 mondrians to cycle through
                mondN = 0           
        if blinking:
            if frameN % int(REFRESH_RATE * 0.6) < REFRESH_RATE / 3.0 + 4:
                if frameN < 10 * REFRESH_RATE:
                    monds1[mondN].draw()
                    monds2[mondN].draw()
                if frameN % int(REFRESH_RATE * 0.6) >= 2 and frameN % int(REFRESH_RATE * 0.6) < REFRESH_RATE / 3.0 + 2:
                    stim.draw()
        else:
            stim.draw()
            if frameN < 10 * REFRESH_RATE:
                monds1[mondN].draw()
                monds2[mondN].draw()
        if event.getKeys(keyList=['space']):
            breakingTime = time.time() - startTime
            win.flip()
            break
        win.flip()
    if askLocation:
        passedTask = askForLocation(stimLoc, False)   
        print str(color) + ': ' + str(breakingTime) + ' seconds, test passed=' + str(passedTask)
        OUTPUT_FILE.write(str(color).replace(' ', '') + ' ' + str(stimLoc) + ' ' + str(breakingTime) + ' ' + str(passedTask) + '\n')
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
    current = 0
    ranksUsed = 0
    while ranksUsed < len(colorsToTest):
        indicator.pos = (circles[colorsToTest[current]].pos[0], 0.175)
        win.flip()
        input = event.waitKeys(keyList=[str(i) for i in range(1, len(colorsToTest) + 1)] + ['left', 'right'])
        if input[0] == 'left' and current > 0:
            current -= 1
        elif input[0] == 'right' and current < len(colorsToTest) - 1:
            current += 1
        elif input[0] in [str(i) for i in range(1, len(colorsToTest) + 1)] :       
            for color in colorsToTest:
                if ranks[color].text == input[0]:
                    ranks[color].text = '_'  # erase previous choice for that rank
                    ranksUsed -= 1
            if ranks[colorsToTest[current]].text == '_':
                ranksUsed += 1
            ranks[colorsToTest[current]].text = input[0]
        event.clearEvents()   
    OUTPUT_FILE.write('preferences: ')
    for color in colorsToTest:
        OUTPUT_FILE.write(str(color).replace(' ', '') + str(ranks[color].text) + ' ')
    OUTPUT_FILE.write('\n')
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
    '''CURRENTLY UNUSED: Employs heterochromatic flicker photometry to return equiluminant colors of given hues.'''
    def multiplyTuple(c, factor):
        return (int(c[0] * factor), int(c[1] * factor), int(c[2] * factor))
    flickerer.autoDraw = True
    sliderBar.autoDraw = True
    origScale = max(color2) / 255.0
    scaleFactor = origScale
    #  Reusing the indicator object
    indicator.pos = (-0.3 + scaleFactor * 0.6, -0.2)
    indicator.size = (0.01, 0.02 * ASPECT_RATIO)
    indicator.autoDraw = True
    instructions.text = 'Press the left and right arrow keys to adjust the luminance of the colors. When' + \
                        ' the circle does not seem to flicker anymore, press space to continue.'    
    temp2 = multiplyTuple(color2, scaleFactor / origScale)
    while not event.getKeys(keyList=['space']):
        flickerer.fillColor = color1
        flickerer.lineColor = color1
        for frameN in range(REFRESH_RATE / 60):  # show each color for 1/60th of a second
            win.flip()
        flickerer.fillColor = temp2
        flickerer.lineColor = temp2
        for frameN in range(REFRESH_RATE / 60):
            win.flip()
        input = event.getKeys(keyList=['left', 'right'])
        if input and input[0] == 'left':
            if scaleFactor > 0.01:
                scaleFactor -= 0.01
                indicator.pos = (-0.3 + scaleFactor * 0.6, -0.2)
            temp2 = multiplyTuple(color2, scaleFactor / origScale)
        elif input and input[0] == 'right':
            if scaleFactor < 0.99:
                scaleFactor += 0.01
                indicator.pos = (-0.3 + scaleFactor * 0.6, -0.2)
            temp2 = multiplyTuple(color2, scaleFactor / origScale)
    event.clearEvents()
    instructions.autoDraw = False
    flickerer.autoDraw = False
    sliderBar.autoDraw = False
    indicator.autoDraw = False
    return (color1, temp2)
    
def equiluminanceAlt(color1, color2):
    '''Employs minimum motion technique to return equiluminant colors of given hues.'''
    def multiplyTuple(c, factor):
        return (int(round(c[0] * factor)), int(round(c[1] * factor)), int(round(c[2] * factor)))
    motionGrating1.autoDraw = True
    motionGrating2.autoDraw = True
    sliderBar.autoDraw = True
    origScale = 0.5
    scaleFactor = origScale
    #  Reusing the indicator object
    indicator.pos = (-0.3 + scaleFactor * 0.6, -0.2)
    indicator.size = (0.01, 0.02 * ASPECT_RATIO)
    indicator.autoDraw = True
    instructions.text = 'Press the left and right arrow keys to adjust the luminance of the colors. When' + \
                        " the pattern's movement seems to change direction, press space to continue."    
    temp2 = multiplyTuple(color2, scaleFactor / origScale)
    framesPerCycle = REFRESH_RATE / 3
    scaleStep = 0.1
    global msk1, msk2
    while not event.getKeys(keyList=['space']):
        for frameN in range(framesPerCycle):
            if frameN == 0 or frameN == framesPerCycle / 2:
                msk1 *= -1
                msk2 *= -1
            if frameN % (framesPerCycle / 2) < framesPerCycle / 4:
                motionGrating1.color = color1
                motionGrating2.color = temp2
                motionGrating1.mask = msk1
                motionGrating2.mask = -msk1
            else:
                motionGrating1.color = (0, 0, 0)
                motionGrating2.color = (8, 8, 8)
                motionGrating1.mask = msk2
                motionGrating2.mask = -msk2
            win.flip()                         
            input = event.getKeys(keyList=['left', 'right'])
            if input and input[0] == 'left':
                if scaleFactor > scaleStep:
                    scaleFactor -= scaleStep
                    indicator.pos = (-0.3 + scaleFactor * 0.6, -0.2)
                temp2 = multiplyTuple(color2, scaleFactor / origScale)
            elif input and input[0] == 'right':
                if scaleFactor < 1 - scaleStep:
                    scaleFactor += scaleStep
                    indicator.pos = (-0.3 + scaleFactor * 0.6, -0.2)
                temp2 = multiplyTuple(color2, scaleFactor / origScale)
    event.clearEvents()
    instructions.autoDraw = False
    motionGrating1.autoDraw = False
    motionGrating2.autoDraw = False
    sliderBar.autoDraw = False
    indicator.autoDraw = False
    OUTPUT_FILE.write('equiluminantColor: ' + str(temp2).replace(' ', '') + '\n') 
    return (color1, temp2)

def rotatedSineTexture(degrees):
    '''Returns numpy array of grating texture rotated from vertical by given amount of degrees.'''
    tex1 = np.zeros((256, 256))
    slope = np.arctan(degrees * np.pi / 180)  # gabor is rotated by degree amount in layout
    for y in range(256):
        for x in range(256):
            dist = (-slope * (y - 128) + (x - 128)) / np.sqrt(1 + slope ** 2)
            val1 = np.sin(dist * 2.0 * np.pi / 256 * 4)  # spatial frequency (sine periods)      
            tex1[y][x] = val1
    return tex1

def calibrateDifficulty():
    '''
    Returns tilt of gabor patch such that orientation task accuracy is around 75%. 
    Staircases down from 5 degrees and then up from 1 degree, then averages results.
    '''
    def tiltStaircase(tilt, loweringTilt):
        for reversal in range(10):
            correctStreak = 0
            while True:               
                gabor.pos = (-CENTER_DIST, YPOS + (np.random.randint(0, 2) - 0.5) * 0.24 + LEFT_SHIFT)
                dir = (np.random.randint(0, 2) - 0.5) * 2.0
                gabor.tex = rotatedSineTexture(tilt * dir)
                waitForReady(True)
                waitPeriod = np.random.randint(REFRESH_RATE / 2, REFRESH_RATE + 1)
                for frameN in range(waitPeriod):
                    drawBackground()
                    win.flip()
                for frameN in range(REFRESH_RATE / 5):
                    drawBackground()
                    gabor.draw()
                    win.flip()
                passedTask = askForLocation(dir, True)
                showConfirmation()
                if passedTask:
                    correctStreak += 1
                    if correctStreak == 3:
                        correctStreak = 0
                        if abs(tilt) > 0.1:
                            tilt -= 0.5
                            if not loweringTilt:
                                loweringTilt = True
                                break
                else:
                    correctStreak = 0
                    tilt += 0.5
                    if loweringTilt:
                        loweringTilt = False
                        break
        return tilt
    tilt1 = tiltStaircase(5.0, True)
    return (tilt1 + tiltStaircase(1.0, False)) / 2.0
                
def ringPrime(stimColor, ringColor, popLoc):
    '''
    Presents a suppressed ring of 8 cross-circles as a prime. The top cross-circle is of a different color.
    DEPRECATED: Returns whether or not the subject indicated (by pressing space) that they saw the ring. 
    '''
    for mond in monds1:
        mond.size = (0.25, 0.25 * ASPECT_RATIO)
        mond.pos = (CENTER_DIST, YPOS)
    stim.size = (0.018, 0.018 * ASPECT_RATIO)  # reusing same stim object from first experiment
    stim.pos = (-CENTER_DIST, YPOS + popLoc + LEFT_SHIFT)
    stim.color = stimColor
    primingRing.colors = ringColor
    primingRing.fieldPos = (-CENTER_DIST, YPOS + LEFT_SHIFT)
    mondN = 0
    for frameN in range(int(2.5 * REFRESH_RATE)):  
        if int(frameN % (REFRESH_RATE / 10.0)) == 0:  # change mondrian 10 times per second
            mondN += 1            
            if mondN > 9:  # there are 10 mondrians to cycle through
                mondN = 0
            #monds1[mondN].opacity = np.random.randint(70, 101) / 100.0
        drawBackground()
        if frameN % int(REFRESH_RATE * 0.5) < REFRESH_RATE / 5 + 6:
            if frameN < 10 * REFRESH_RATE:
                monds1[mondN].draw()
            if frameN % int(REFRESH_RATE * 0.5) >= 3 and frameN % int(REFRESH_RATE * 0.5) < REFRESH_RATE / 5 + 3:
                stim.opacity = (frameN % int(REFRESH_RATE * 0.5) - 2) / (REFRESH_RATE / 5.0 + .01)
                primingRing.opacities = (frameN % int(REFRESH_RATE * 0.5) - 2) / (REFRESH_RATE / 5.0 + .01)
                primingRing.draw()
                stim.draw()
        rightFixBorder.draw()
        rightFix1.draw()
        rightFix2.draw()
        '''
        if event.getKeys(keyList=['space']):
            event.clearEvents()
            return True
        '''
        win.flip()
    return False

def askVisible():
    '''
    Draws the question asking whether the subject saw the prime and waits for subject to answer.
    Returns subjective visibility level (0, 1, or 2) as a string.
    '''
    event.clearEvents()
    questionL.text = 'Did you see any circles with crosses?'
    questionR.text = 'Did you see any circles with crosses?'
    current = 0
    while True:
        indicatorL.pos = (-CENTER_DIST, -current * 0.045 + YPOS - 0.045 + LEFT_SHIFT)
        indicatorR.pos = (CENTER_DIST, -current * 0.045 + YPOS - 0.045)
        drawBackground()
        indicatorL.draw()
        indicatorR.draw()
        questionL.draw()
        optionsL.draw()
        questionR.draw()
        optionsR.draw()
        win.flip()  
        answer = event.waitKeys(keyList=['up', 'down', 'space'])
        if answer[0] == 'up' and current > 0:
            current -= 1
        elif answer[0] == 'down' and current < 2:
            current += 1
        elif answer[0] == 'space':
            break
    return str(current)

def askLocationsSeen():
    '''Lets the subject select areas in which they saw patches and returns selections.'''
    event.clearEvents()
    questionL.text = '\n\n\n\n\n\nUse the up and down arrow keys to indicate where in \n\nthe box you ' + \
                     'saw the circles in, then press space to submit.'
    questionR.text = '\n\n\n\n\n\nUse the up and down arrow keys to indicate where in \n\nthe box you ' + \
                     'saw the circles in, then press space to submit.'
    upSelected, downSelected = False, False
    while True:
        drawBackground()
        if upSelected:
            upperHalfL.draw()
            upperHalfR.draw()
        if downSelected:
            lowerHalfL.draw()
            lowerHalfR.draw()
        questionL.draw()
        questionR.draw()
        win.flip()
        answer = event.waitKeys(keyList=['up', 'down', 'space'])
        if answer[0] == 'up':
            upSelected = not upSelected
        elif answer[0] == 'down':
            downSelected = not downSelected
        elif answer[0] == 'space':
            break
    return (upSelected, downSelected)
    
def askColorSeen(color1, color2):
    '''Draws the question asking what suppressed colors were seen and waits for subject to answer.'''
    event.clearEvents()
    stimL1.color = color1
    stimL2.color = color2
    stimR1.color = color1
    stimR2.color = color2
    drawBackground()
    questionL.text = 'Which of the following colors did you see?'
    questionR.text = 'Which of the following colors did you see?'
    choicesL.text = '\n\n\n\n(L)                 (R)\n\n  Both (space)'
    choicesR.text = '\n\n\n\n(L)                 (R)\n\n  Both (space)'
    questionL.draw()
    choicesL.draw()
    stimL1.draw()
    stimL2.draw()
    questionR.draw()
    choicesR.draw()
    stimR1.draw()
    stimR2.draw()
    win.flip()
    answer = event.waitKeys(keyList=['left', 'right', 'space'])
    return answer[0]
    
def orientationTask(color1, color2, layout):  
    '''
    Runs a full trial of measuring the speed of performing an orientation task
    after a pop-out prime of the given colors at the location determined by
    the given layout tuple. Writes results to output text file.
    
    Layout tuple format: 
    (color of the popout cross, location (top or bottom) of popout, location of gabor, clockwise tilt of gabor)
    '''
    tex1 = rotatedSineTexture(abs(layout[3]))
    tex2 = rotatedSineTexture(-abs(layout[3]))
    waitForReady(True)
    if layout[0] == 1:
        primeVisible = ringPrime(color1, color2, layout[1])
    else:
        primeVisible = ringPrime(color2, color1, layout[1])
    if not primeVisible:
        gabor.pos = (-CENTER_DIST, YPOS + layout[2] + LEFT_SHIFT)
        if layout[3] > 0:
            gabor.tex = tex1
        else:
            gabor.tex = tex2        
        startTime = time.time()
        for frameN in range(int(REFRESH_RATE / 5)):
            drawBackground()
            gabor.draw()
            win.flip()
        passedTask = askForLocation(layout[3], True) 
        responseTime = time.time() - startTime
        OUTPUT_FILE.write(str(layout) + ' ' + str(responseTime) + ' ' + str(passedTask) + ' ' + askVisible() + 
                          ' ' + str(askLocationsSeen()).replace(' ', '') + ' ' + askColorSeen(color1, color2) + '\n')
        event.clearEvents()
    showConfirmation()
    
def showEndMsg():
    '''Displays message signifying the end of the experiment and waits for quit.'''
    endMsg.draw()
    win.flip()
    event.waitKeys(keyList=['q', 'escape'])
    
    
if __name__ == '__main__':
    print "Running at " + str(win.size) + " resolution with refresh rate of " + str(win.getActualFrameRate()) + " Hz..."
    print "Conducting experiment 1 using the following colors: " + str(colorsToTest)
    OUTPUT_FILE.write('START1\n')
    # All possible trial configurations for first experiment
    layouts = []
    for color in colorsToTest:
        for stimLoc in [-0.0625, 0.0625]:
            layouts.append((color, stimLoc))
    trialOrder = []
    for i in range(len(layouts)):
        trialOrder += [i] * FIRST_STAGE_REPETITIONS
    np.random.shuffle(trialOrder)
    for layoutN in trialOrder:
        circleBreakingTime(layouts[layoutN][0], layouts[layoutN][1], True, True)
    OUTPUT_FILE.write('END1\n')
        
    extremes = recordPreference(colorsToTest)
    newColors = equiluminanceAlt(extremes[0], extremes[1])
    #tiltMag = calibrateDifficulty()
    tiltMag = 5
    print "Optimal tilt magnitude calibrated to be: " + str(tiltMag) + " degrees..."
    
    OUTPUT_FILE.write('START2\n')
    # All possible trial configurations for second experiment
    layouts = []
    for popColor in [1, 2]:
        for popLoc in [-ringRadius, ringRadius]:
            for gabLoc in [-ringRadius, ringRadius]:
                for gabTilt in [-tiltMag, tiltMag]:
                    layouts.append((popColor, popLoc, gabLoc, gabTilt))
    trialOrder = []
    for i in range(len(layouts)):
        trialOrder += [i] * SECOND_STAGE_REPETITIONS
    np.random.shuffle(trialOrder)
    for layoutN in trialOrder:
        orientationTask(newColors[0], newColors[1], layouts[layoutN])
    OUTPUT_FILE.write('END2\n')
    showEndMsg()
    
# Global cleanup
cleanExit()