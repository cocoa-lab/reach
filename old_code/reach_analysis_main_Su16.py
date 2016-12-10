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
from math import sqrt
import glob

from reach_analysis_functions_Su16 import graph_var_by_cond_between, get_LR_lev_frames, get_stat_frames, create_folder, graph_pokeTime_by_cond_within
from reach_analysis_functions_Su16 import get_x_var, get_y_var, get_standard_train1_frame, get_standard_train2_frame, graph_releaseTime_by_cond_within
from reach_analysis_functions_Su16 import graph_by_val_sep_test_within, graph_by_sep_test_within,  get_standard_test_frame
#global variables at top
from reach_analysis_functions_Su16 import *
all_subs = []
input_dir ='data/'

BETWEEN_SUB_GRAPH_DIR = '\\graphs\\between\\'


SMALL_ABS_SEP  = 32
LARGE_ABS_SEP  = 44
ZERO_PEN       = 0
SMALL_PEN      = -1
LARGE_PEN      = -5
MULT_SMALL_PEN = -3
MULT_LARGE_PEN = -15

#all_e_subs = glob.glob('*_reach_train_output.csv')

for n in range(300, 400):
    try: 
        temp_frame = pd.read_csv('%s%s_reach_test_output.csv' % (input_dir, n), index_col=0)
        if n != 999:
            all_subs.append(n)
    except: 
        continue

def main():

    #all_levs_frame     = DataFrame()
    #all_LR_Y_lev_frame = DataFrame()
    #all_LR_X_lev_frame = DataFrame()
    all_vars_frame     = DataFrame()
    all_dists_frame    = DataFrame()
    all_pokes_frame    = DataFrame()
    all_scores_frame   = DataFrame()
    all_optimals_frame = DataFrame()
    all_test_frames    = DataFrame()

    all_stat_frames = [all_vars_frame, all_dists_frame, all_pokes_frame, all_scores_frame, all_optimals_frame]

    for sub in all_subs: 

        temp_output_directory = '\\graphs\\%s\\' % (sub)
        create_folder(temp_output_directory)

        temp_test_frame  = get_standard_test_frame(sub)
        temp_stat_frames = get_stat_frames(temp_test_frame)
        temp_stat_frames.append(temp_test_frame)
        temp_vars = temp_stat_frames[0]

        #graph_by_val_sep_test_within(temp_test_frame, temp_output_directory)

        # temp_LR_lev_frames  = get_LR_lev_frames(temp_test_frame)
        # LR_X_lev_frame      = temp_LR_lev_frames[0]
        # LR_Y_lev_frame      = temp_LR_lev_frames[1]
        # temp_levs           = temp_stat_frames[0]
        # temp_levs['subNum'] = sub
        # all_levs_frame      = pd.concat([all_levs_frame, temp_levs])
        # all_LR_Y_lev_frame  = pd.concat([all_LR_Y_lev_frame, LR_Y_lev_frame])
        # all_LR_X_lev_frame  = pd.concat([all_LR_X_lev_frame, LR_X_lev_frame])
        #LR_X_lev_frame['subNum'] = sub
        #LR_Y_lev_frame['subNum'] = sub

        
        optimal_dict       = {'32,0': [], '44,0': [],  '32,1': [],'44,1': [],  '32,3': [],  '44,3': [], '32,5': [],  '44,5': [],  '32,15': [],'44,15': []}
        optimal_aim_points = []
        
        n = 0
        #temp_points = [(-80, 0), (-60, 0), (-15, 0), (30, 0), (50, 0), (-70, 0), (-5, 0)]
        for condition in temp_vars: 

            print "Condition: " + condition
            print "----------------------------"
            temp_std = sqrt(temp_vars[condition].sum()) 
            print "getting ev array..."
            temp_ev_array  = get_EV_array(temp_std, condition)
            print "getting optimal point..."
            temp_opt_point_ev  = get_opt_point_ev(temp_ev_array)
            temp_optimal_point = temp_opt_point_ev[0]
            optimal_dict[condition]  = [temp_optimal_point]
            print "getting EV landscape..."
            create_EV_landscape(temp_ev_array, condition, temp_output_directory, temp_opt_point_ev)
            
            # # if n == 3:
            # #     1/0
            # # else: 
            # #     n += 1

  
        temp_optimals = pd.DataFrame(dict([(k,Series(v)) for k,v in optimal_dict.iteritems()]))
        
        temp_stat_frames.append(temp_optimals)

        temp_vars['subNum'] = sub
        
        pd.concat([all_vars_frame, temp_vars])
        pd.concat([all_optimals_frame, temp_optimals])

    print all_optimals_frame
    
    all_vars_frame.to_csv('all_vars_by_cond_table.csv')
    all_optimals_frame.to_csv('all_optimals_by_cond.csv')



    #graph_var_by_cond_between(all_vars_frame, BETWEEN_SUB_GRAPH_DIR)
    


    1/0    

    
if __name__ == '__main__':
    main()
        
       




    
