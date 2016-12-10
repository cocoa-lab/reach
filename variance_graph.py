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

from reach_analysis_functions_Fa16_graph import graph_var_by_cond_between, get_LR_lev_frames, get_stat_frames, create_folder, graph_pokeTime_by_cond_within
from reach_analysis_functions_Fa16_graph import get_x_var, get_y_var, get_standard_train1_frame, get_standard_train2_frame, graph_releaseTime_by_cond_within
from reach_analysis_functions_Fa16_graph import graph_by_val_sep_test_within, graph_by_sep_test_within,  get_standard_test_frame
#global variables at top
from reach_analysis_functions_Fa16_graph import *
all_subs = []
input_dir ='data/'

BETWEEN_SUB_GRAPH_DIR = '\\graphs\\between\\300'

for n in range(300, 450):
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
    all_vars_frame           = DataFrame()

    for sub in all_subs:

    	temp_test_frame   = get_standard_test_frame(sub)
        
        temp_stat_frames  = get_stat_frames(temp_test_frame)

        temp_vars         = temp_stat_frames[0]
        temp_vars['subNum'] = sub 

    	all_vars_frame     = pd.concat([all_vars_frame, temp_vars])

    all_vars_frame.to_csv('34cond_var.csv')

    graph_var_by_cond_between(all_vars_frame, BETWEEN_SUB_GRAPH_DIR)


    
if __name__ == '__main__':
    main()
