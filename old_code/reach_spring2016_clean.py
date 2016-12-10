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
from pyglet.window import key, Window
from psychopy.iohub import launchHubServer
import winsound


#this reads in the data frame of circle configurations
testInfo = pd.DataFrame.from_csv('test_new.csv')

#set standard timeLimit. This assumes it is the same for every trial in block
TRIAL_TIME_LIMIT = testInfo.iloc[0]['timeLimit']

#Use this to turn on and off the tone signal
USE_BEEP = False

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

# Start the ioHub process. The return variable is what is used
# during the experiment to control the iohub process itself,
# as well as any running iohub devices.
io=launchHubServer()

# By default, ioHub will create Keyboard and Mouse devices and
# start monitoring for any events from these devices only.
keyboard = io.devices.keyboard
mouse = event.Mouse(visible=True, win=win)

# # store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

#mouse    = event.Mouse(win=win)

#initialize transparent background shape; passing this shape is necessary for executing the mouse.isPressedIn() function
background = visual.Polygon(win=win, name='background',
    edges = 4, size=[2000, 2000],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[255, 255, 0], lineColorSpace='rgb',
    fillColor=[255, 255, 0], fillColorSpace='rgb',
    opacity=0,depth=-1.0, 
    interpolate=True)

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
    lineWidth=1, lineColor=[-1, -1, 1], lineColorSpace='rgb',
    fillColor=[-1, -1, 1], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
    interpolate=True)

target = visual.Polygon(win=win, name='target',
    edges = 90, size=[64, 64],
    ori=0, pos=[0, 0],
    lineWidth=5, lineColor=[-1, 1, -1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=0.0, 
    interpolate=True)

penalty_color = visual.Polygon(win=win, name='penalty_color', edges = 4, 
    size = [64, 64], ori = 180, pos = [-64, 0], lineWidth = 5, 
    lineColor = [1, -1, -1], lineColorSpace = 'rgb', 
    fillColor = [1, -1, -1], fillColorSpace = 'rgb',
    opacity = 1, depth = -1, interpolate = True)
reward_color = visual.Polygon(win=win, name='reward_color', edges = 4, 
    size = [64, 64], ori = 180, pos = [64, 0], lineWidth = 5, 
    lineColor = [-1, 1, -1], lineColorSpace = 'rgb', 
    fillColor = [-1, 1, -1], fillColorSpace = 'rgb',
    opacity = 1, depth = -1, interpolate = True)


penalty = visual.Polygon(win=win, name='penalty',
    edges = 90, size=[64, 64],
    ori=0, pos=[-32, 0],
    lineWidth=5, lineColor=[1, -1, -1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
    interpolate=True)

cross_horizontal = visual.Polygon(win=win, name='horiz',
    edges = 2, size=[60, 60],
    ori=0, pos=[0, 0], 
    lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1, 1, 1], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
    interpolate=True)

cross_vertical = visual.Polygon(win=win, name='vertic',
    edges = 2, size=[60, 60],
    ori=90, pos=[0, 0],
    lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1, 1, 1], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
    interpolate=True)

#text objects

no_poke_text       = visual.TextStim(win, text = u"Too Slow!")
 
too_soon_text      = visual.TextStim(win, text = u"You Reached Too Soon \n\nWait For Target")

test_text          = visual.TextStim(win, text = u"")

press_text         = visual.TextStim(win, pos=(0,50), text='Hold down the SPACEBAR...')
 
penalty_value      = visual.TextStim(win, pos=(-64, 64), text=' ')

reward_value       = visual.TextStim(win, pos=(64, 64), text=' ')

block_point_feed   = visual.TextStim(win, pos = (0, -100), text = '')

total_point_feed   = visual.TextStim(win, pos = (0, -200), text = '')

encourage_feed     = visual.TextStim(win, pos = (0, 200), text =  '')

train_instructions = visual.TextStim(win, pos = (0, 0), text = '')
train_instructions.setSize(200, units='pixels')

test_instructions  = visual.TextStim(win, pos = (0, 50), text = 'Nice job! Check out your scores:')

trial_point_feed   = visual.TextStim(win, pos = (0, 200), text = '')
# no_poke_text = visual.TextStim(win=win, ori=0, name='text',
#     text=u'Too slow!',    font=u'Arial',
#     pos=[0, 0], height=0.1, wrapWidth=None,
#     color=u'white', colorSpace='rgb', opacity=1,
#     depth=-2.0)

# Create some handy timers
globalClock          = core.Clock()  # to track the time since experiment started
routineTimer         = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
TestClock            = core.Clock()
trainingClock        = core.Clock()
blue_fix_timer       = core.CountdownTimer()
aim_dot_timer        = core.CountdownTimer()
feedback_timer       = core.CountdownTimer()
value_display_timer  = core.CountdownTimer()
train_instr_timer    = core.CountdownTimer()
test_instr_timer     = core.CountdownTimer()
feedback_timer       = core.CountdownTimer()
point_feed_timer     = core.CountdownTimer()


#create lists for storing training data
aimDotPositions    = []
pokePositionsTrain = []
pokeDistancesTrain = []
trialNumsTrain     = []
pokeTimesTrain     = []            

current_train_block = 0
total_train_block   = 3
print "before first while loop"
#TRAING BLOCKS
while current_train_block < total_train_block:

    current_train_trial = 0
    total_train_trial   = 1
    poke_num = 0

    train_instr_timer.reset()
    train_instr_timer.add(5)
    train_instr_text = 'You are about to begin block ' + str(current_train_block + 1) + ' of ' + str(total_train_block) + '.\n When the yellow dot appears, try to poke it with your finger. Please press ENTER to continue.'
    train_instructions.setText(train_instr_text)

    while not keyboard.state.has_key('z'):
        
        train_instructions.draw() 
        win.flip()

        # check for quit (the Esc key)
        if keyboard.state.has_key('escape'):
            core.quit()

    #TRAINING LOOP
    while current_train_trial < total_train_trial:

        poke_now = False
        poked = False
        released_too_soon = False
        
        #------Prepare to start Routine "training"-------
        t = 0
        trainingClock.reset()  # clock 
        frameN = -1

        #duration of the trial; to change trial duration, modify the value below, as well as the value in each component update
        

        #random or uniform distribution?
        aim_pos_x = random.randrange(-160, 161) 
        aim_pos_y = random.randrange(-160, 161)

        train_aim_dot.pos = [aim_pos_x, aim_pos_y]
        #-------Start Routine "training"-------
        continueRoutine   = True

        space_pressed = False

        #change fixation color to white
        cross_vertical.fillColor   = [1, 1, 1]
        cross_horizontal.fillColor = [1, 1, 1]
        cross_vertical.lineColor   = [1, 1, 1]
        cross_horizontal.lineColor = [1, 1, 1]

        #FIXATION CROSS
        #Ends when spacebar is pressed
        while not keyboard.state.has_key(' '):
            # test_text.setText(str(keyboard.state))
            # test_text.draw()
            cross_vertical.draw()
            cross_horizontal.draw()
        #Ends after time period between 400 and 600 ms
        while blue_fix_timer.getTime() > 0:

            #make fixation cross blue
            cross_vertical.fillColor = [-1, -1, 1]
            cross_horizontal.fillColor = [-1, -1, 1]
            cross_vertical.lineColor = [-1, -1, 1]
            cross_horizontal.lineColor = [-1, -1, 1]

            cross_vertical.draw()
            cross_horizontal.draw()

            if not keyboard.state.has_key(' '):
                released_too_soon = True
            press_text.draw()
            win.flip()

              # check for quit (the Esc key)
            if keyboard.state.has_key('escape'):
                core.quit()

        press_time = trainingClock.getTime()

        blue_fix_timer.reset()

        blue_fix_timer.add(random.uniform(.4, .6))


        #BLUE FIXATION CROSS

            # check for quit (the Esc key)
        if keyboard.state.has_key('escape'):
            core.quit()
              
            win.flip()
        print "after fixation"
        #INITIAL TARGET VIEWING
        if USE_BEEP:
            view_time = .4
            aim_dot_timer.reset()
            aim_dot_timer.add(view_time)
            
            while aim_dot_timer.getTime() > 0 and not released_too_soon:
                train_aim_dot.draw()

                if not keyboard.state.has_key(' '):
                    released_too_soon = True
                win.flip()

        #initialize mouse position to bottom center of screen
        mouse.setPos([0, -899])

        #reset timers
        aim_dot_timer.reset()
        aim_dot_timer.add(TRIAL_TIME_LIMIT)

        #if needed start beep signal
        if USE_BEEP:
            Freq = 1000 # Set Frequency To 1000 Hertz
            Dur = 400 # Set Duration To 400 ms == 1 second
            winsound.Beep(Freq,Dur)


        #TARGET VIEWING AND READ-IN
        while aim_dot_timer.getTime() > 0 and not released_too_soon:
            # get current time
            t = trainingClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

            
            train_aim_dot.draw()
            background.draw()

            
            
            # check for quit (the Esc key)
            if keyboard.state.has_key('escape'):
                core.quit()

            # if not keyboard.state.has_key(' ') and aim_dot_timer.getTime() > .6:
            #     released_too_soon = True
            #     release_time = aim_dot_timer.getTime()
            # elif not keyboard.state.has_key(' ') and aim_dot_timer.getTime() < .6:
            #     release_time = aim_dot_timer.getTime()

            # don't flip if this routine is over or we'll get a blank screen
            win.flip()

            # true iff poke occured at this frame within boundaries of 'background', i.e., anywhere in window
            poke_now = mouse.isPressedIn(background, buttons=[0]) and  not keyboard.state.has_key(' ')
            
            #if poke occured at this frmae, then prepare to draw poke_dot at that the poke location at next frame and store time elapsed since trial start
            if poke_now: 
                poked            = True
                poke_pos         = mouse.getPos()
                poke_dot.pos     = poke_pos
                poke_time_train  = t # rename to rt of some sort
                poke_dot.draw() # Draw poke position immediately potentially for touch screen debugging
                

        feedback_timer.reset()

        feedback_timer.add(3.5)
        
        #FEEDBACK
        while feedback_timer.getTime() > 0:

            # *poke_dot* updates
            if poked:
               poke_dot.draw()
               train_aim_dot.draw()
            elif released_too_soon:
                too_soon_text.draw()
            else: 
                no_poke_text.draw()   

            # check for quit (the Esc key)
            if keyboard.state.has_key('escape'):
                core.quit()
            
            win.flip()

            
        #in case there was no poke in the previous trial, add empty values to RT and poke position lists
        if poked: 
            poke_distance = dist(train_aim_dot.pos, poke_dot.pos)
            poke_pos      = poke_dot.pos
            poke_pos      = poke_pos.tolist()
        else:
            poke_distance    = float('nan')
            poke_time_train  = float('nan')
            poke_pos         = float('nan') 
      
        
        #increment after each trial
        if not released_too_soon:
            current_train_trial += 1
                #add training data to lists
            pokeDistancesTrain.append(poke_distance)
            train_aim_dot_position = train_aim_dot.pos.tolist()
            aimDotPositions.append(train_aim_dot_position)
            pokePositionsTrain.append(poke_pos)
            trialNumsTrain.append(current_train_trial)
            pokeTimesTrain.append(poke_time_train)

                    #create dictionary from training data lists and dataframe from this dictionary
            train_data_dict  = {'aimDotPos': aimDotPositions, 'pokePos': pokePositionsTrain, 'trial': trialNumsTrain, 'pokeTime': pokeTimesTrain, 'pokeDist': pokeDistancesTrain}
            train_data_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in train_data_dict.iteritems()]))
            train_data_frame.to_csv(_thisDir + '/data/%s_reach_train_output.csv' % (expInfo['participant']))


    current_train_block += 1
        
#radius of the circles
radius = 32


#create lists to store test data
scores            = []
pokePositionsTest = []
penaltyPositions  = []
targetPositions   = []
penaltyDistances  = []
targetDistances   = []
pokeTimesTest     = [] #rename to have RT
trialNumber       = []
blockNumber       = []
targetSizes       = []
sepDistances      = []
rewardValue       = []
penaltyValue      = []
timeLimits        = []
withinStimBools   = []  # 1 == poked within stimulus config. , 0 == poked outside stim. config. , NaN if no poke
accuracies        = []  # 1 == target poke, 0 == middle poke, -1 == penalty poke, NaN == else (i.e., too slow or outside config.)
tooSlowBools      = []  # 1 == too slow, 0 == not too slow




#start out with zero total points
total_points = 0

#TEST

#BLOCK LOOP
current_test_block = 0
total_test_block   = 5 #This number can be less than the number of blocks in dataframe but not more
trials_per_block = len(testInfo.index) / (testInfo.iloc[len(testInfo.index) - 1]["blockNum"] + 1) #length of dataframe / number of blocks in dataframe

while current_test_block < total_test_block:
    # start block with zero block points
    block_points = 0

    #initialize mouse position to bottom center of screen
    mouse.setPos([0, -899])


    test_instr_timer.reset()
    test_instr_timer.add(7)
    test_instr_text = 'You are about to begin block ' + str(current_test_block + 1) + ' of ' + str(total_test_block) + '. \nTry to earn as many points as you can by poking the green target circle with your finger.'
    test_instructions.setText(test_instr_text)

    while test_instr_timer.getTime() > 0:
        test_instructions.draw()
        win.flip()

        # check for quit (the Esc key)
        if keyboard.state.has_key('escape'):
            core.quit()

    #TRIAL LOOP
    #duration of test
    current_test_trial = int(trials_per_block * current_test_block)
    total_test_trial = current_test_trial + trials_per_block
    
    while current_test_trial < total_test_trial:
        #------Prepare to start Routine "Test"-------
        poke_time_test = 0
        t = 0
        TestClock.reset()  # clock 
        
        #Get and set positioning 
        sep_dis = testInfo.iloc[current_test_trial]['sepDistance']
        targ_pos_x = testInfo.iloc[current_test_trial]['x_position']
        targ_pos_y = testInfo.iloc[current_test_trial]['y_position']
        target.pos  = [targ_pos_x, targ_pos_y]
        penalty.pos = [targ_pos_x + sep_dis, targ_pos_y] # no magic numbers

        #Get and set reward/penalty values
        rew_value = testInfo.iloc[current_test_trial]['reward']
        pen_value = testInfo.iloc[current_test_trial]['penalty']

        poked    = False
        poke_now = False
        released_too_soon = False

        #-------Start Routine "Test"-------

        space_pressed = False

        #change fixation color to white
        cross_vertical.fillColor   = [1, 1, 1]
        cross_horizontal.fillColor = [1, 1, 1]
        cross_vertical.lineColor   = [1, 1, 1]
        cross_horizontal.lineColor = [1, 1, 1]

        #reward/penalty display
        value_display_timer.reset()
        value_display_timer.add(2)
        penalty_value.setText(str(pen_value))
        reward_value.setText('+' + str(rew_value))
        while value_display_timer.getTime() > 0:

            penalty_value.draw()
            reward_value.draw()
            penalty_color.draw()
            reward_color.draw()

            win.flip()



            # check for quit (the Esc key)
            if keyboard.state.has_key('escape'):
                core.quit()

        #FIXATION CROSS
        #Ends when spacebar is pressed
        while not keyboard.state.has_key(' '):
            # test_text.setText(str(keyboard.state))
            # test_text.draw()
            cross_vertical.draw()
            cross_horizontal.draw()
            press_text.draw()

            win.flip()

              # check for quit (the Esc key)
            if keyboard.state.has_key('escape'):
                core.quit()

        press_time = TestClock.getTime()

        blue_fix_timer.reset()
        blue_fix_timer.add(random.uniform(.4, .6))
        
        #BLUE FIXATION CROSS
        #Ends after time period between 400 and 600 ms
        while blue_fix_timer.getTime() > 0:

            #make fixation cross blue
            cross_vertical.fillColor = [-1, -1, 1]
            cross_horizontal.fillColor = [-1, -1, 1]
            cross_vertical.lineColor = [-1, -1, 1]
            cross_horizontal.lineColor = [-1, -1, 1]

            cross_vertical.draw()
            cross_horizontal.draw()

            if not keyboard.state.has_key(' '):
                released_too_soon = True

            # check for quit (the Esc key)
            if keyboard.state.has_key('escape'):
                core.quit()
              
            win.flip()
        
        #INITIAL TARGET VIEWING
        if USE_BEEP:
            view_time = .4
            routineTimer.reset()
            routineTimer.add(view_time)
            
            while routineTimer.getTime() > 0 and not released_too_soon:
                target.draw()
                penalty.draw()

                if not keyboard.state.has_key(' '):
                    released_too_soon = True
                win.flip()
        
        routineTimer.reset()
        routineTimer.add(TRIAL_TIME_LIMIT)
        continueRoutine = True
        TestClock.reset()

        #initialize mouse position to bottom center of screen
        mouse.setPos([0, -899])
        
        #if needed start beep signal
        if USE_BEEP:
            Freq = 1000 # Set Frequency To 2500 Hertz
            Dur = 400 # Set Duration To 1000 ms == 1 second
            winsound.Beep(Freq,Dur)

        #MAIN LOOP: POKE HERE!
        while continueRoutine and routineTimer.getTime() > 0 and not released_too_soon:
            # get current time
            t = TestClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
           
            background.draw()
            target.draw()
            penalty.draw()
            
            # check for quit (the Esc key)
            if keyboard.state.has_key('escape'):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

            #true iff poke occured at this frame within boundaries of 'background', i.e., anywhere in window AND the spacebar was released
            poke_now = mouse.isPressedIn(background, buttons=[0]) and  not keyboard.state.has_key(' ')

            #if poke occurred at this frame, then prepare to draw poke_dot at that the poke location next frame and store time elapsed since trial start
            if poke_now: 
                poked        = True
                poke_pos     = mouse.getPos()
                poke_dot.pos = poke_pos
                poke_time_test  = t
                continueRoutine = False 

         #in case there was no poke in the previous trial, add empty values to RT, poke position, and distance lists
        if poked:
            penalty_distance = dist(penalty.pos, poke_dot.pos)
            target_distance  = dist(target.pos, poke_dot.pos)
            poke_pos         = poke_pos.tolist()
        else: 
            poke_time_test   = float('nan')
            poke_pos         = float('nan')
            penalty_distance = float('nan')
            target_distance  = float('nan')

        #determines whether poke occured within target region, penalty region, overlap region, or outside of stimulus structure
        target_poke  = (penalty_distance > radius) and (target_distance < radius)
        penalty_poke = (penalty_distance < radius) and (target_distance > radius)
        mix_poke     = (penalty_distance < radius) and (target_distance < radius)
        miss_poke    = (penalty_distance > radius) and (target_distance > radius)

        #assign points based on what region the poke occured within
        if released_too_soon:
            points     = float('nan')
            accuracy   = float('nan')
            withinStim = float('nan')
            tooSlow    = 0
        elif target_poke:
            points     = rew_value # MAGIC NUMBERS  
            accuracy   = 1
            withinStim = 1
            tooSlow    = 0
        elif penalty_poke:
            points     = pen_value
            accuracy   = -1
            withinStim = 1
            tooSlow    = 0
        elif mix_poke:
            points     = rew_value + pen_value
            accuracy   = 0
            withinStim = 1
            tooSlow    = 0
        elif miss_poke:
            points = 0
            accuracy = float('nan')
            withinStim = 0
            tooSlow = 0
        else: 
            points     = -700
            tooSlow    = 1
            withinStim = 0
            accuracy   = float('nan')


        if points > 0:
            point_text = '+ ' + str(points) 
            trial_point_feed.setColor([-1, 1, -1], colorSpace = 'rgb')
        elif points < 0:
            point_text = str(points)
            trial_point_feed.setColor([1, -1, -1], colorSpace = 'rgb')
        else:
            point_text = str(points)


        continueRoutine = True
        TestClock.reset()  # clock 
        routineTimer.add(2)

        frameCount = 0
        

        trial_point_feed.setText(point_text)
        #FEEDBACK LOOP
        while routineTimer.getTime() > 0:

            # get current time
            t = TestClock.getTime()
            
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
            # change opacity of the circles every 10 frames, to give the appearance of flashing, based on where poke occurred
            frameCount = int(frameN/10)
            
            if released_too_soon:
                too_soon_text.draw()
            elif poked:
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
                no_poke_text.draw()

            # refresh the screen
            win.flip()

            trial_point_feed.draw()

            # check for quit (the Esc key)
            if keyboard.state.has_key('escape'):
                core.quit()
                     
        target.opacity  = 1
        penalty.opacity = 1

        if not released_too_soon:
            #convert np.ndarray positions to lists
            target_position  = target.pos.tolist()
            penalty_position = penalty.pos.tolist()
            #add data to lists
            penaltyDistances.append(penalty_distance)
            targetDistances.append(target_distance)
            scores.append(points)
            pokePositionsTest.append(poke_pos)
            penaltyPositions.append(penalty_position)
            targetPositions.append(target_position)
            pokeTimesTest.append(poke_time_test) #time distance from beginning of trial to poke
            
            trial_in_block = total_test_trial - current_test_trial - 1 #trial number within current block (0-17)
            trialNumber.append(trial_in_block)

            targetSizes.append(target.size[0]) #diameter
            blockNumber.append(current_test_block)
            rewardValue.append(rew_value)
            penaltyValue.append(pen_value)
            sepDistances.append(sep_dis)
            timeLimits.append(TRIAL_TIME_LIMIT)
            withinStimBools.append(withinStim)
            accuracies.append(accuracy)
            tooSlowBools.append(tooSlow)

                        #create dictionary from test data lists and dataframe from this dictionary
            test_data_dict  = {'score': scores, 'pokePos': pokePositionsTest, 'penaltyPos': penaltyPositions, 'targDist': targetDistances,
                               'penalDist': penaltyDistances, 'targetPos': targetPositions, 'pokeTime': pokeTimesTest, 'trial': trialNumber, 'block': blockNumber, 'targSize': targetSizes, 
                               'sepDist' : sepDistances, 'rewardVal': rewardValue, 'penaltyVal': penaltyValue, 'tooSlow': tooSlowBools, 'accuracy': accuracies, 'withinStimulus': withinStimBools}
            test_data_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in test_data_dict.iteritems()]))
            test_data_frame.to_csv(_thisDir + '/data/%s_reach_test_output.csv' % (expInfo['participant']))


            #increment block points after each successful trial
            block_points += points

            #increment to next trial
            current_test_trial += 1

        else:#if they did release to soon, place this trial at the end of the block to be tried again
            if current_test_trial == 0:
                testInfo = pd.concat([testInfo.ix[1:total_train_trial], testInfo.ix[[0]], testInfo.ix[total_train_trial:]])
                testInfo = testInfo.reset_index(drop=True)
            elif total_test_trial < len(testInfo.index):
                testInfo = pd.concat([testInfo.ix[0:current_test_trial - 1], 
                            testInfo.ix[current_test_trial + 1:total_train_trial], testInfo.ix[[current_test_trial]], testInfo.ix[total_train_trial:]])
                testInfo = testInfo.reset_index(drop=True)
            else:
                testInfo = pd.concat([testInfo.ix[0:current_test_trial - 1], testInfo.ix[current_test_trial + 1:], testInfo.ix[[current_test_trial]]])
                testInfo = testInfo.reset_index(drop=True)
    
    total_points += block_points

    current_test_block += 1

    #timed feedback slide after each block
    point_feed_timer.reset()
    point_feed_timer.add(5)
    block_point_feed.setText('Points in previous block: ' + str(block_points))
    total_point_feed.setText('Total points: ' + str(total_points))

    while point_feed_timer.getTime() > 0:

        encourage_feed.draw()
        block_point_feed.draw()
        total_point_feed.draw()
        win.flip()






win.close()
core.quit()
