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
all_subs_test = []
all_subs_train = []
input_dir='data/'
output_dir= 'output/'
#all_e_subs = glob.glob('*_reach_train_output.csv')
all_subs = [304]


for sub in all_subs:
    try:
        temp_frame_test = pd.read_csv('%s%s_reach_train_output.csv' % (input_dir, sub), index_col=0)
        all_subs_train.append(sub)
    except:
        continue

for sub in all_subs:
    try: 
        temp_frame_train = pd.read_csv('%s%s_reach_test_output.csv' % (input_dir, sub), index_col=0)
        all_subs_test.append(sub)
    except: 
        continue

def main():

    test_frame  = DataFrame()
    train_frame = DataFrame()


    for sind, sub in enumerate(all_subs_train): 
        curr_frame_train      = pd.read_csv('%s%s_reach_train_output.csv' % (input_dir, sub), index_col=0)
        train_frame       = pd.concat([train_frame, curr_frame_train])

    for sind, sub in enumerate(all_subs_test): 
        curr_frame_test       = pd.read_csv('%s%s_reach_test_output.csv' % (input_dir, sub), index_col=0)
        test_frame        = pd.concat([test_frame, curr_frame_test])

    

    standard_pokes_x = []
    standard_pokes_y = []
    absolute_pokes_x = []
    absolute_pokes_y = []

    for n in range(0, len(test_frame.index)):
        
        temp_targ_pos = test_frame.iloc[n]['targetPos']
        temp_poke_pos = test_frame.iloc[n]['pokePos']

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

        standard_pokes_x.append(standard_poke_pos_x)
        standard_pokes_y.append(standard_poke_pos_y)
        absolute_pokes_x.append(abs_poke_pos_x)
        absolute_pokes_y.append(abs_poke_pos_y)


    test_frame['standardPokePosX'] = standard_pokes_x
    test_frame['standardPokePosY'] = standard_pokes_y

    test_frame['absolutePokePosX'] = absolute_pokes_x
    test_frame['absolutePokePosY'] = absolute_pokes_y




    train_stand_pokes_x = []
    train_stand_pokes_y = []


    for n in range(0, len(train_frame.index)):
        
        temp_targ_pos = train_frame.iloc[n]['aimDotPos']
        temp_poke_pos = train_frame.iloc[n]['pokePos']

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
    


    train_frame['standardPokePosX'] = train_stand_pokes_x
    train_frame['standardPokePosY'] = train_stand_pokes_y


    #variability from training
    
    x_var = np.nanvar(train_frame.standardPokePosX)
    y_var = np.nanvar(train_frame.standardPokePosY)



    #GRAPHS OF POKE POSITIONS FOR EACH SEPARATION DISTANCE
    
    #separation 1: 32 pixels to right
    x_poke_sep_1R    = test_frame[test_frame['sepDist'] == -32].standardPokePosX
    y_poke_sep_1R    = test_frame[test_frame['sepDist'] == -32].standardPokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_sep_1R
    y = y_poke_sep_1R
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_sep_1R.mean()
    avg_y = y_poke_sep_1R.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((-32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven1R.pdf',bbox_inches='tight')
    plt.close(fig)


    #separation 2: 32*1.5 pixels to right
    x_poke_sep_1_5R  = test_frame[test_frame['sepDist'] == -1.25*32].standardPokePosX
    y_poke_sep_1_5R  = test_frame[test_frame['sepDist'] == -1.5*32].standardPokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_sep_1_5R
    y = y_poke_sep_1_5R
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_sep_1_5R.mean()
    avg_y = y_poke_sep_1_5R.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((1.5*-32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven1_5R.pdf',bbox_inches='tight')
    plt.close(fig)


    #separation 3: 32*1.25 pixels to right
    x_poke_sep_1_25R = test_frame[test_frame['sepDist'] == -1.25*32].standardPokePosX
    y_poke_sep_1_25R = test_frame[test_frame['sepDist'] == -1.25*32].standardPokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_sep_1_25R
    y = y_poke_sep_1_25R
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_sep_1_25R.mean()
    avg_y = y_poke_sep_1_25R.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((1.25*-32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven1_25R.pdf',bbox_inches='tight')
    plt.close(fig)


    #separation 4: 32 pixels to left
    x_poke_sep_1L    = test_frame[test_frame['sepDist'] == 32].standardPokePosX
    y_poke_sep_1L    = test_frame[test_frame['sepDist'] == 32].standardPokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_sep_1L
    y = y_poke_sep_1L
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_sep_1L.mean()
    avg_y = y_poke_sep_1L.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven1L.pdf',bbox_inches='tight')
    plt.close(fig)



    #separation 5: 1.5*32 pixels to left
    x_poke_sep_1_5L  = test_frame[test_frame['sepDist'] == 1.5*32].standardPokePosX
    y_poke_sep_1_5L  = test_frame[test_frame['sepDist'] == 1.5*32].standardPokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_sep_1_5L
    y = y_poke_sep_1_5L
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_sep_1_5L.mean()
    avg_y = y_poke_sep_1_5L.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((1.5*32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven1_5L.pdf',bbox_inches='tight')
    plt.close(fig)



    #separation 6: 1.25*32 pixels to left
    x_poke_sep_1_25L = test_frame[test_frame['sepDist'] == 1.25*32].standardPokePosX
    y_poke_sep_1_25L = test_frame[test_frame['sepDist'] == 1.25*32].standardPokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))
    
    x = x_poke_sep_1_25L
    y = y_poke_sep_1_25L
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_sep_1_25L.mean()
    avg_y = y_poke_sep_1_25L.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((1.25*32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven1_25L.pdf',bbox_inches='tight')
    plt.close(fig)




    #GRAPHS OF POKE POSITION FOR EACH PENALTY VALUE

    #penalty 1: value of 0
    x_poke_val_0 = test_frame[test_frame['penaltyVal'] == 0].absolutePokePosX
    y_poke_val_0 = test_frame[test_frame['penaltyVal'] == 0].absolutePokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_val_0
    y = y_poke_val_0
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_val_0.mean()
    avg_y = y_poke_val_0.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((-32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven_val_0.pdf',bbox_inches='tight')
    plt.close(fig)


    #penalty 2: value of -100
    x_poke_val_100 = test_frame[test_frame['penaltyVal'] == -100].absolutePokePosX
    y_poke_val_100 = test_frame[test_frame['penaltyVal'] == -100].absolutePokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))

    x = x_poke_val_100
    y = y_poke_val_100
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_val_100.mean()
    avg_y = y_poke_val_100.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((-32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven_val_100.pdf',bbox_inches='tight')
    plt.close(fig)

    #penalty 3: value of -500
    x_poke_val_500 = test_frame[test_frame['penaltyVal'] == -500].absolutePokePosX
    y_poke_val_500 = test_frame[test_frame['penaltyVal'] == -500].absolutePokePosY

    ax = plt.gca()
    fig = plt.gcf()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))
 
    x = x_poke_val_500
    y = y_poke_val_500
    plt.plot(x, y, "o", color='black')

    avg_x = x_poke_val_500.mean()
    avg_y = y_poke_val_500.mean()
    plt.plot((avg_x), (avg_y), 'o', color = 'y')
    avg_mark = plt.Circle((avg_x, avg_y), 5,color='b',fill=False)

    target  = plt.Circle((0,0), 32,color='g',fill=False)
    penalty = plt.Circle((-32,0), 32, color='r', fill=False) 
    
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(output_dir + 'ven_val_500.pdf',bbox_inches='tight')
    plt.close(fig)



    

    
    

    # fig.gca().add_artist(penalty)
    # fig.gca().add_artist(target)
    # fig.savefig('plotcircles2.png')

    1/0

    
if __name__ == '__main__':
    main()