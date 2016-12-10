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

from reach_analysis_functions_Fa16 import graph_var_by_cond_between, get_LR_lev_frames, get_stat_frames, create_folder, graph_pokeTime_by_cond_within
from reach_analysis_functions_Fa16 import get_x_var, get_y_var, get_standard_train1_frame, get_standard_train2_frame, graph_releaseTime_by_cond_within
from reach_analysis_functions_Fa16 import graph_by_val_sep_test_within, graph_by_sep_test_within,  get_standard_test_frame
#global variables at top
from reach_analysis_functions_Fa16 import *
all_subs = []
input_dir ='data/'

BETWEEN_SUB_GRAPH_DIR = '\\graphs\\between\\'


for n in range(403, 450):
    try: 
        temp_frame = pd.read_csv('%s%s_reach_test_output.csv' % (input_dir, n), index_col=0)
        if n != 999:
            all_subs.append(n)
    except: 
        continue



def main():

	print "Please ensure that there exists a ev_array.csv file for the subject, condition, and model of interest"
	print "_____________________________________________________________________________________________"

	sub_in  = input("Please type the subject code and press enter (Form: integer or 'all')")
	cond_in = input("Please type the condition code and press enter (Form: 'sep,pen' or 'all')")
	mod_in  = input("Please type the model code and press enter (Form: 'CN', 'CL', 'RN', 'RL', 'TN', 'TL' or 'all')")

    if sub_in == 'all':
    	subs = all_subs
    else:
    	subs = [sub_in]

    if mod_in == 'all':
    	mods = MODEL_CODES
    else:
    	mods = [mod_in]

    if cond_in = 'all':
    	conds  = CONDITION_LABELS
    else:
    	conds  = cond_in

    for mod in mods:
    	for sub in subs:
    		temp_output_directory = '\\graphs\\%s\\' % (sub)
            create_folder(temp_output_directory)
    		for cond in conds:
    			ev_array = read_csv.('%s_%s_%s_ev_array.csv' (sub, cond, mod))
				print "generating EV landscape..."
				create_EV_landscape(temp_ev_array, cond, temp_output_directory)
    

	#graph_var_by_cond_between(all_vars_frame, BETWEEN_SUB_GRAPH_DIR)

    
if __name__ == '__main__':
    main()
