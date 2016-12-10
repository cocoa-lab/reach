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

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = u'malohney'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

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

# Initialize components for Routine "trial"
trialClock = core.Clock()
mouse = event.Mouse(win=win)
x, y = [None, None]
train_dot = visual.Polygon(win=win, name='train_dot',
    edges = 90, size=[10, 10],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[255, 255, 0], lineColorSpace='rgb',
    fillColor=[255, 255, 0], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)
background = visual.Polygon(win=win, name='train_dot',
    edges = 4, size=[900, 900],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[255, 255, 0], lineColorSpace='rgb',
    fillColor=[255, 255, 0], fillColorSpace='rgb',
    opacity=0,depth=-1.0, 
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

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
train_loop = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='train_loop')
thisExp.addLoop(train_loop)  # add the loop to the experiment
thisTrain_loop = train_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrain_loop.rgb)
if thisTrain_loop != None:
    for paramName in thisTrain_loop.keys():
        exec(paramName + '= thisTrain_loop.' + paramName)

# setup some python lists for storing info about the mouse
mouse.x = []
mouse.y = []
mouse.leftButton = []
mouse.midButton = []
mouse.rightButton = []
mouse.time = []

radius = 32

target_location  = [0, 0]
penalty_location = [-32, 0]



for thisTrain_loop in train_loop:
    currentLoop = train_loop
    # abbreviate parameter names if possible (e.g. rgb = thisTrain_loop.rgb)
    if thisTrain_loop != None:
        for paramName in thisTrain_loop.keys():
            exec(paramName + '= thisTrain_loop.' + paramName)
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    routineTimer.add(10.000000)
    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(mouse)
    #trialComponents.append(background)
    trialComponents.append(train_dot)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine   = True
    mouse_clicked = False
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

         # *mouse* updates
        if t >= 0.0 and mouse.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse.tStart = t  # underestimates by a little under one frame
            mouse.frameNStart = frameN  # exact frame index
            mouse.status = STARTED
            event.mouseButtons = [0, 0, 0]  # reset mouse buttons to be 'up'
        if mouse.status == STARTED and t >= (0.0 + (10-win.monitorFramePeriod*0.75)): #most of one frame period left
            mouse.status = STOPPED
        if mouse.status == STARTED:  # only update if started and not stopped!
            buttons = mouse.getPressed()
            if sum(buttons) > 0:  # ie if any button is pressed
                x, y = mouse.getPos()
                mouse.x.append(x)
                mouse.y.append(y)
                mouse.leftButton.append(buttons[0])
                mouse.midButton.append(buttons[1])
                mouse.rightButton.append(buttons[2])
                mouse.time.append(trialClock.getTime())
                # abort routine on response
                continueRoutine = False
        
        # *train_dot* updates
        if t >= 0.0 and train_dot.status == NOT_STARTED:
            # keep track of start time/frame for later
            train_dot.tStart = t  # underestimates by a little under one frame
            train_dot.frameNStart = frameN  # exact frame index
            train_dot.setAutoDraw(True)
        if train_dot.status == STARTED and t >= (0.0 + (10-win.monitorFramePeriod*0.75)): #most of one frame period left
            train_dot.setAutoDraw(False)

        # *background* updates
        # if t >= 0.0 and background.status == NOT_STARTED:
        #     # keep track of start time/frame for later
        #     background.tStart = t  # underestimates by a little under one frame
        #     background.frameNStart = frameN  # exact frame index
        #     background.setAutoDraw(True)
        # if background.status == STARTED and t >= (0.0 + (10-win.monitorFramePeriod*0.75)): #most of one frame period left
        #     background.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponecnt in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

        # ev = pygame.event.get()

        # for event in ev:
        #     if event.type == pygame.MOUSEBUTTONUP:
        #          mouse_clicked = True

        #mouse_clicked = mouse.isPressedIn(background, buttons=[0])
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for train_loop (TrialHandler)
    x, y = mouse.getPos()
    buttons = mouse.getPressed()
    train_loop.addData('mouse.x', x)
    train_loop.addData('mouse.y', y)
    train_loop.addData('mouse.leftButton', buttons[0])
    train_loop.addData('mouse.midButton', buttons[1])
    train_loop.addData('mouse.rightButton', buttons[2])
    thisExp.nextEntry()
    
# completed 100 repeats of 'train_loop'


# set up handler to look after randomisation of conditions etc
test_loop = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='test_loop')
thisExp.addLoop(test_loop)  # add the loop to the experiment
thisTest_loop = test_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTest_loop.rgb)
if thisTest_loop != None:
    for paramName in thisTest_loop.keys():
        exec(paramName + '= thisTest_loop.' + paramName)

for thisTest_loop in test_loop:
    currentLoop = test_loop
    # abbreviate parameter names if possible (e.g. rgb = thisTest_loop.rgb)
    if thisTest_loop != None:
        for paramName in thisTest_loop.keys():
            exec(paramName + '= thisTest_loop.' + paramName)
    
    #------Prepare to start Routine "Test"-------
    t = 0
    TestClock.reset()  # clock 
    frameN = -1
    routineTimer.add(10.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    TestComponents = []
    TestComponents.append(target)
    TestComponents.append(penalty)
    for thisComponent in TestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Test"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = TestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

         # *mouse* updates
        if t >= 0.0 and mouse.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse.tStart = t  # underestimates by a little under one frame
            mouse.frameNStart = frameN  # exact frame index
            mouse.status = STARTED
            event.mouseButtons = [0, 0, 0]  # reset mouse buttons to be 'up'
        if mouse.status == STARTED and t >= (0.0 + (10-win.monitorFramePeriod*0.75)): #most of one frame period left
            mouse.status = STOPPED
        if mouse.status == STARTED:  # only update if started and not stopped!
            buttons = mouse.getPressed()
            if sum(buttons) > 0:  # ie if any button is pressed
                x, y = mouse.getPos()
                mouse.x.append(x)
                mouse.y.append(y)
                mouse.leftButton.append(buttons[0])
                mouse.midButton.append(buttons[1])
                mouse.rightButton.append(buttons[2])
                mouse.time.append(trialClock.getTime())
                # abort routine on response
                continueRoutine = False
            
        # *target* updates
        if t >= 0.0 and target.status == NOT_STARTED:
            # keep track of start time/frame for later
            target.tStart = t  # underestimates by a little under one frame
            target.frameNStart = frameN  # exact frame index
            target.setAutoDraw(True)
        if target.status == STARTED and t >= (0.0 + (10-win.monitorFramePeriod*0.75)): #most of one frame period left
            target.setAutoDraw(False)
        
        # *penalty* updates
        if t >= 0.0 and penalty.status == NOT_STARTED:
            # keep track of start time/frame for later
            penalty.tStart = t  # underestimates by a little under one frame
            penalty.frameNStart = frameN  # exact frame index
            penalty.setAutoDraw(True)
        if penalty.status == STARTED and t >= (0.0 + (10-win.monitorFramePeriod*0.75)): #most of one frame period left
            penalty.setAutoDraw(False)
        
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
    
    #-------Ending Routine "Test"-------
    for thisComponent in TestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 5 repeats of 'test_loop'

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort() # or data files will save again on exit
win.close()
core.quit()
