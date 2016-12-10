#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.83.04), May 11, 2016, at 14:16
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys # to get file system encoding
import pygame
import math # math needed for sqrt
import pandas as pd
from pandas import DataFrame, Series
import random
# distance function
def dist(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = u'malohney'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u''}
dlg     = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date']    = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=[900, 900], fullscr=False, screen=0, allowGUI=True, allowStencil=False,
    monitor=u'testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

#initialize transparent background shape; passing this shape is necessary for executing the mouse.isPressedIn() function,
#which returns True iff a given mouse button is pressed in within a given shape 
background = visual.Polygon(win=win, name='background',
    edges = 4, size=[2000, 2000],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[255, 255, 0], lineColorSpace='rgb',
    fillColor=[255, 255, 0], fillColorSpace='rgb',
    opacity=0,depth=-1.0, 
interpolate=True)

# Initialize components for Routine "training"
trainingClock = core.Clock()
mouse = event.Mouse(win=win)
x, y = [None, None]
train_aim_dot = visual.Polygon(win=win, name='train_aim_dot',
    edges = 90, size=[10, 10],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[255, 255, 0], lineColorSpace='rgb',
    fillColor=[255, 255, 0], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)
poke_dot = visual.Polygon(win=win, name='poke_dot',
    edges = 90, size=[10, 10],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[0, 0, 255], lineColorSpace='rgb',
    fillColor=[0, 0, 255], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)

# Initialize components for Routine "Test"
TestClock = core.Clock()
target = visual.Polygon(win=win, name='target',
    edges = 90, size=[64, 64],
    ori=0, pos=[0, 0],
    lineWidth=5, lineColor=[0,255,0], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=0.0, 
interpolate=True)
penalty = visual.Polygon(win=win, name='penalty',
    edges = 90, size=[64, 64],
    ori=0, pos=[-32, 0],
    lineWidth=5, lineColor=[255,0,0], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)

feedback_text = visual.TextStim(win, text = u"Too Slow!")
# feedback_text = visual.TextStim(win=win, ori=0, name='text',
#     text=u'Too slow!',    font=u'Arial',
#     pos=[0, 0], height=0.1, wrapWidth=None,
#     color=u'white', colorSpace='rgb', opacity=1,
#     depth=-2.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#create lists for storing training data
aimDotPositions    = []
pokePositionsTrain = []
trialNumsTrain     = []
pokeTimesTrain     = []

current_train_trial = 1
total_train_trial   = 2

poked   = False
poke_now = False

while current_train_trial <= total_train_trial:
    
    #------Prepare to start Routine "training"-------
    t = 0
    trainingClock.reset()  # clock 
    frameN = -1

    #duration of the trial; to change trial duration, modify the value below, as well as the value in each component update, e.g., the 2 in 
    #"if mouse.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75))"
    routineTimer.add(2.000000)


    # keep track of which components have finished
    trainingComponents = []
    trainingComponents.append(mouse)
    trainingComponents.append(background)
    trainingComponents.append(train_aim_dot)
    trainingComponents.append(poke_dot)

    for thisComponent in trainingComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #random or uniform distribution?
    aim_pos_x = random.randrange(-160, 161)
    aim_pos_y = random.randrange(-160, 161)

    train_aim_dot.pos = [aim_pos_x, aim_pos_y]
    #-------Start Routine "training"-------
    continueRoutine   = True

    #keyboard.getKeys(keylist='spacebar', timeStamped = False)

    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = trainingClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

         # *mouse* updates
        if t >= 0.0 and mouse.status == NOT_STARTED:
            mouse.status       = STARTED
            event.mouseButtons = [0, 0, 0]  # reset mouse buttons to be 'up'
        if mouse.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
            mouse.status = STOPPED
        
        # *train_aim_dot* updates
        if t >= 0.0 and train_aim_dot.status == NOT_STARTED:
            train_aim_dot.setAutoDraw(True)
        if train_aim_dot.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
            train_aim_dot.setAutoDraw(False)

        # *poke_dot* updates
        if t >= 0.0 and poke_dot.status == NOT_STARTED and poke_now:
            # keep track of start time/frame for later
            poke_dot.tStart      = t  # underestimates by a little under one frame
            poke_dot.frameNStart = frameN  # exact frame index
            poke_dot.setAutoDraw(True)
        if poke_dot.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
            poke_dot.setAutoDraw(False)

        #*background* updates
        if t >= 0.0 and background.status == NOT_STARTED:
            # keep track of start time/frame for later
            background.tStart      = t  # underestimates by a little under one frame
            background.frameNStart = frameN  # exact frame index
            background.setAutoDraw(True)
        if background.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
            background.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running

        for thisComponecnt in trainingComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

        # true iff poke occured at this frame within boundaries of 'background', i.e., anywhere in window
        poke_now = mouse.isPressedIn(background, buttons=[0])
        
        #if poke occured at this frmae, then prepare to draw poke_dot at that the poke location at next frame and store time elapsed since trial start
        if poke_now: 
            poked    = True
            poke_dot.pos     = mouse.getPos()
            poke_time_train  = t

    
    #-------Ending Routine "training"-------
    for thisComponent in trainingComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    #in case there was no poke in the previous trial, add empty values to RT and poke position lists
    if not poked:
        poke_time_train  = float('nan')
        poke_pos         = float('nan')

    #add training data to lists
    aimDotPositions.append(train_aim_dot.pos)
    pokePositionsTrain.append(poke_dot.pos)
    trialNumsTrain.append(current_train_trial)
    pokeTimesTrain.append(poke_time_train)

    #increment after each trial
    current_train_trial += 1
  
# completed 10 repeats of 'train_trial'

current_test_trial = 1
total_test_trial   = 10

#radius of the circles
radius = 32


#create lists to store test data
scores            = []
pokePositionsTest = []
penaltyPositions  = []
targetPositions   = []
pokeTimesTest     = []
trialNumsTest     = []
targetSizes       = []



while current_test_trial <= total_test_trial:
    #------Prepare to start Routine "Test"-------
    poke_time_test = 0
    t = 0
    TestClock.reset()  # clock 
    frameN = -1
    routineTimer.add(2)
    # update component parameters for each repeat
    # keep track of which components have finished
    TestComponents = []
    TestComponents.append(target)
    TestComponents.append(penalty)
    TestComponents.append(poke_dot)
    TestComponents.append(background)
    for thisComponent in TestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #random or uniform distribution?
    targ_pos_x = random.randrange(-160, 161)
    targ_pos_y = random.randrange(-160, 161)

    target.pos  = [targ_pos_x, targ_pos_y]
    penalty.pos = [targ_pos_x - 32, targ_pos_y]

    poked    = False
    poke_now = False
    
    #-------Start Routine "Test"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = TestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
       
         # *mouse* updates
        if t >= 0.0 and mouse.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse.tStart       = t  # underestimates by a little under one frame
            mouse.frameNStart  = frameN  # exact frame index
            mouse.status       = STARTED
            event.mouseButtons = [0, 0, 0]  # reset mouse buttons to be 'up'
        if mouse.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
            mouse.status = STOPPED

        # *target* updates
        if t >= 0.0 and target.status == NOT_STARTED:
            # keep track of start time/frame for later
            target.tStart       = t  # underestimates by a little under one frame
            target.frameNStart  = frameN  # exact frame index
            target.setAutoDraw(True)
        if target.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
            target.setAutoDraw(False)
        
        # *penalty* updates
        if t >= 0.0 and penalty.status == NOT_STARTED:
            # keep track of start time/frame for later
            penalty.tStart       = t  # underestimates by a little under one frame
            penalty.frameNStart  = frameN  # exact frame index
            penalty.setAutoDraw(True)
        if penalty.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
            penalty.setAutoDraw(False)

        #*background* updates
        if t >= 0.0 and background.status == NOT_STARTED:
            # keep track of start time/frame for later
            background.tStart       = t  # underestimates by a little under one frame
            background.frameNStart  = frameN  # exact frame index
            background.setAutoDraw(True)
        if background.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
            background.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

        #true iff poke occured at this frame within boundaries of 'background', i.e., anywhere in window
        poke_now = mouse.isPressedIn(background, buttons=[0])

        #if poke occured at this frame, then prepare to draw poke_dot at that the poke location next frame and store time elapsed since trial start
        if poke_now: 
            poked  = True
            poke_dot.pos    = mouse.getPos()
            poke_time_test  = t
            continueRoutine = False 

    #-------Ending Routine "Test"-------

    for thisComponent in TestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    #calculate distance between poke and center of target and penalty regions
    poke_pos = poke_dot.pos
    penalty_distance = dist(penalty.pos, poke_pos)
    target_distance  = dist(target.pos, poke_pos)

    #determines whether poke occured within target region, penalty region, overlap region, or outside of stimulus structure
    target_poke  = (penalty_distance > radius) and (target_distance < radius)
    penalty_poke = (penalty_distance < radius) and (target_distance > radius)
    mix_poke     = (penalty_distance < radius) and (target_distance < radius)
    miss_poke    = (penalty_distance > radius) and (target_distance > radius)

    #assign points based on what region the poke occured within
    if target_poke:
        points = 1
    elif penalty_poke:
        points = -2
    elif mix_poke:
        points = -1
    elif miss_poke:
        points = 0

    #in case there was no poke in the previous trial, add empty values to RT and poke position lists
    if not poked:
        poke_time_train  = float('nan')
        poke_pos         = float('nan')

    #add data to lists
    scores.append(points)
    pokePositionsTest.append(poke_pos)
    penaltyPositions.append(penalty.pos)
    targetPositions.append(target.pos)
    pokeTimesTest.append(poke_time_test) #time distance from beginning of trial to poke
    trialNumsTest.append(current_test_trial)
    targetSizes.append(target.size[0]) #diameter

    current_test_trial += 1

    continueRoutine = True
    TestClock.reset()  # clock 
    routineTimer.add(2)

    frameCount = 0

    for thisComponent in TestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    while routineTimer.getTime() > 0:

        # get current time
        t = TestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        frameCount = int(frameN/10)

        
        if poked:
            if mix_poke and not (frameCount % 2):
                target.opacity  = 1
                penalty.opacity = 1
            elif mix_poke and (frameCount % 2): 
                target.opacity  = 0
                penalty.opacity = 0
            elif penalty_poke and not (frameCount % 2):
                target.opacity  = 1
                penalty.opacity = 1
            elif penalty_poke and (frameCount % 2):
                target.opacity  = 1
                penalty.opacity = 0
            elif target_poke and not (frameCount % 2):
                target.opacity  = 1
                penalty.opacity = 1
            elif target_poke and (frameCount % 2):
                target.opacity  = 0
                penalty.opacity = 1
            elif miss_poke:
                target.opacity  = 1
                penalty.opacity = 1
            poke_dot.draw()
            target.draw()
            penalty.draw()  
        else:
            feedback_text.draw()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
                 
    target.opacity  = 1
    penalty.opacity = 1





#create dictionary from training data lists and dataframe from this dictionary
train_data_dict  = {'aimDotPos': aimDotPositions, 'pokePos': pokePositionsTrain, 'trial': trialNumsTrain, 'pokeTime': pokeTimesTrain}
train_data_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in train_data_dict.iteritems()]))
train_data_frame.to_csv(_thisDir + '/data/%s_reach_train_output.csv' % (expInfo['participant']), sep= '\t')

#create dictionary from test data lists and dataframe from this dictionary
test_data_dict  = {'score': scores, 'pokePos': pokePositionsTest, 'penaltyPos': penaltyPositions,
                  'targetPos': targetPositions, 'pokeTime': pokeTimesTest, 'trial': trialNumsTest}
test_data_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in test_data_dict.iteritems()]))
test_data_frame.to_csv(_thisDir + '/data/%s_reach_test_output.csv' % (expInfo['participant']), sep= '\t')
    

win.close()
core.quit()
