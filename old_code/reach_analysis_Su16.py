import numpy as np
import pandas as pd 
import scipy as sp 
import os 
import matplotlib as mpl
from scipy.stats import ttest_ind
from pandas import Series, DataFrame
from matplotlib import pyplot as plt
from matplotlib import style
from scipy import stats
from matplotlib import rcParams
from ast import literal_eval
import matplotlib.pyplot as plt
import math
import glob


# rcParams.update({'figure.autolayout': True})
style.use('fivethirtyeight')

#global variables at top
all_subs = []
input_dir ='data/'

RADIUS = 32 #pixels
SMALL_ABS_SEP  = 32
LARGE_ABS_SEP  = 44
ZERO_PEN       = 0
SMALL_PEN      = -1
LARGE_PEN      = -5
MULT_SMALL_PEN = -3
MULT_LARGE_PEN = -15

#all_e_subs = glob.glob('*_reach_train_output.csv')

for sub in range(300, 400):
    try: 
        temp_frame_train = pd.read_csv('%s%s_reach_test_output.csv' % (input_dir, sub), index_col=0)
        all_subs.append(sub)
    except: 
        continue

def get_standard_train1_frame(subject_number):

    train1_frame  = pd.read_csv('%s%s_reach_train1_output.csv' % (input_dir, subject_number), index_col=0)

    train_stand_pokes_x = []
    train_stand_pokes_y = []

    for n in range(0, len(train1_frame.index)):
        
        temp_targ_pos = train1_frame.iloc[n]['aimDotPos']
        temp_poke_pos = train1_frame.iloc[n]['pokePos']

        if not pd.isnull(temp_poke_pos):

            temp_targ_pos = literal_eval(temp_targ_pos)
            temp_poke_pos = literal_eval(temp_poke_pos) 
            
            standard_poke_pos_x = temp_poke_pos[0] - temp_targ_pos[0] 
            standard_poke_pos_y = temp_poke_pos[1] - temp_targ_pos[1]

        else: 
            standard_poke_pos_x = float('nan')
            standard_poke_pos_y = float('nan')
      
    train_stand_pokes_x.append(standard_poke_pos_x)
    train_stand_pokes_y.append(standard_poke_pos_y)
    

    train1_frame['standardPokePosX'] = train_stand_pokes_x
    train1_frame['standardPokePosY'] = train_stand_pokes_y

    return train1_frame

def get_x_var(train1_frame):

    return np.nanvar(train1_frame.standardPokePosX)

def get_y_var(train1_frame):

    return np.nanvar(train1_frame.standardPokePosY)
    
def get_standard_train2_frame(subject_number):

    train2_frame  = pd.read_csv('%s%s_reach_train2_output.csv' % (input_dir, subject_number), index_col=0)

    standard_pokes_x = []
    standard_pokes_y = []
    absolute_pokes_x = [] 
    absolute_pokes_y = []
    absolute_seps    = []

    for n in range(0, len(test_frame.index)):

        temp_targ_pos = train2_frame.iloc[n]['targetPos']
        temp_poke_pos = train2_frame.iloc[n]['pokePos']
        temp_sep_dist = literal_eval(train2_frame.iloc[n]['sepDist'])

        if not pd.isnull(temp_poke_pos):

            temp_targ_pos = literal_eval(temp_targ_pos)
            temp_poke_pos = literal_eval(temp_poke_pos) 
            
            standard_poke_pos_x = temp_poke_pos[0] - temp_targ_pos[0] 
            standard_poke_pos_y = temp_poke_pos[1] - temp_targ_pos[1]

            abs_poke_pos_x      = abs(standard_poke_pos_x)
            abs_poke_pos_y      = standard_poke_pos_y

        else: 
            standard_poke_pos_x = float('nan')
            standard_poke_pos_y = float('nan')
            abs_poke_pos_y      = float('nan')
            abs_poke_pos_x      = float('nan')

        
        abs_sep = abs(temp_sep_dist)

        standard_pokes_x.append(standard_poke_pos_x)
        standard_pokes_y.append(standard_poke_pos_y)
        absolute_pokes_x.append(abs_poke_pos_x)
        absolute_pokes_y.append(abs_poke_pos_y)
        absolute_seps.append(abs_sep)


    train2_frame['standardPokePosX'] = standard_pokes_x
    train2_frame['standardPokePosY'] = standard_pokes_y

    train2_frame['absolutePokePosX'] = absolute_pokes_x
    train2_frame['absolutePokePosY'] = absolute_pokes_y
    test_frame['absoluteSepDist']  = absolute_seps

    return train2_frame

def get_standard_test_frame(subject_number):
    test_frame    = pd.read_csv('%s%s_reach_test_output.csv' % (input_dir, subject_number), index_col=0)
      
    #standardized poke positions factor out the jittered position of the target   
    standard_pokes_x = []
    standard_pokes_y = []
    #absolute values of the standardized poke positions
    absolute_pokes_x = [] 
    absolute_pokes_y = []
    absolute_seps    = []

    for n in range(0, len(test_frame.index)):
        
        temp_targ_pos = literal_eval(test_frame.iloc[n]['targetPos'])
        temp_poke_pos = test_frame.iloc[n]['pokePos']
        temp_sep_dist = literal_eval(test_frame.iloc[n]['sepDist'])

        if not pd.isnull(temp_poke_pos):

            temp_poke_pos = literal_eval(temp_poke_pos) 
            
            standard_poke_pos_x = temp_poke_pos[0] - temp_targ_pos[0] 
            standard_poke_pos_y = temp_poke_pos[1] - temp_targ_pos[1]

            abs_poke_pos_x      = abs(standard_poke_pos_x)
            abs_poke_pos_y      = standard_poke_pos_y

        else: 
            standard_poke_pos_x = float('nan')
            standard_poke_pos_y = float('nan')
            abs_poke_pos_y      = float('nan')
            abs_poke_pos_x      = float('nan')


        abs_sep = abs(temp_sep_dist)

        standard_pokes_x.append(standard_poke_pos_x)
        standard_pokes_y.append(standard_poke_pos_y)
        absolute_pokes_x.append(abs_poke_pos_x)
        absolute_pokes_y.append(abs_poke_pos_y)
        absolute_seps.append(abs_sep)


    test_frame['standardPokePosX'] = standard_pokes_x
    test_frame['standardPokePosY'] = standard_pokes_y
    test_frame['absolutePokePosX'] = absolute_pokes_x
    test_frame['absolutePokePosY'] = absolute_pokes_y
    test_frame['absoluteSepDist']  = absolute_seps

    return test_frame


def graph_by_sep_test(test_frame, separation_distance, subject_number):

    output_dir = 'graphs/%s/' % (subject_number)

    x_poke_sep    = test_frame[test_frame['absoluteSepDist'] == separation_distance].standardPokePosX
    y_poke_sep    = test_frame[test_frame['absoluteSepDist'] == separation_distance].standardPokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_sep
    y = y_poke_sep
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_sep.mean()
    avg_y = y_poke_sep.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)


    target  = plt.Circle((0,0), RADIUS, color='g',fill=False)
    penalty = plt.Circle((-separation_distance,0), RADIUS, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'sep' + str(separation_distance) + '_test.pdf', bbox_inches='tight')
    plt.close(fig)

def graph_by_val_test(test_frame, penalty_value, subject_number):

    output_dir = 'graphs/%s/' % (subject_number)

    x_poke_val = test_frame[test_frame['penaltyVal'] == penalty_value].absolutePokePosX
    y_poke_val = test_frame[test_frame['penaltyVal'] == penalty_value].absolutePokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_val
    y = y_poke_val
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_val.mean()
    avg_y = y_poke_val.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), RADIUS,color='g',fill=False)
    penalty = plt.Circle((-RADIUS,0), RADIUS, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'pen' + str(abs(penalty_value)) +'_test.pdf',bbox_inches='tight')
    plt.close(fig)



def main():

    for sub in all_subs: 
       
        temp_train1_frame  = get_standard_train1_frame(sub)
        temp_train2_frame  = get_standard_train2_frame(sub)
        temp_test_frame    = get_standard_test_frame(sub)

        temp_x_variability = get_x_var(train1_frame)
        temp_y_variability = get_y_var(train1_frame)

        graph_by_sep_test(temp_test_frame, SMALL_ABS_SEP, sub)
        graph_by_sep_test(temp_test_frame, LARGE_ABS_SEP, sub)

        graph_by_val_test(temp_test_frame, ZERO_PEN, sub)
        graph_by_val_test(temp_test_frame, SMALL_PEN, sub)
        graph_by_val_test(temp_test_frame, LARGE_PEN, sub)
        graph_by_val_test(temp_test_frame, MULT_SMALL_PEN, sub)
        graph_by_val_test(temp_test_frame, MULT_LARGE_PEN, sub)

        1/0

    
if __name__ == '__main__':
    main()
        
       




    
