import numpy as np
import pandas as pd 
import scipy as sp 
import os 
import matplotlib as mpl
from scipy.stats import ttest_ind
from pandas import Series, DataFrame
from matplotlib import pyplot as plt
from scipy import stats
from matplotlib import rcParams
from ast import literal_eval
import matplotlib.pyplot as plt
import math
from math import sqrt
import glob

from reach_analysis_functions_Fa16_graph import get_standard_train1_frame, get_standard_test_frame, get_x_var, get_y_var, get_LA_score, get_stat_frames
all_subs = []
input_dir ='data/'

BETWEEN_SUB_GRAPH_DIR = '\\graphs\\between\\'

current_working_dir = os.getcwd()


#all_e_subs = glob.glob('*_reach_train_output.csv')

for n in range(403, 550):
    try: 
        temp_frame = pd.read_csv('%s%s_reach_test_output.csv' % (input_dir, n), index_col=0)
        if n != 999:
            all_subs.append(n)
    except: 
        continue

def main():

    for sub in all_subs: 

        print "Subject number: " + str(sub)
        print "_________________________________"

        loss_aversion_score = get_LA_score(sub)

        

        temp_test_frame   = DataFrame() #stores standardized test data for one subject
        temp_stat_frames  = DataFrame() #stores stats for all conditions in train1, 2, or test for one subject 

        temp_output_directory = '/standard_data/'
        
        temp_test_frame   = get_standard_test_frame(sub)
        loss_aversion_list = [loss_aversion_score] * len(temp_test_frame.index)
        temp_test_frame["LossAversion"] = loss_aversion_list
        temp_stat_frames  = get_stat_frames(temp_test_frame)

        #mean variance for each condition
        temp_vars         = temp_stat_frames[0]
        
        temp_train1_frame = get_standard_train1_frame(sub)
        train1_x_var      = get_x_var(temp_train1_frame)
        train1_y_var      = get_y_var(temp_train1_frame)
        #mean variance for entire training part 2
        train1_var        = np.mean([train1_x_var, train1_y_var])
        train1_var_list   = [train1_var] * len(temp_test_frame.index)
        temp_test_frame['train1_var'] = train1_var_list


        print temp_test_frame

        temp_vars.to_csv(current_working_dir+temp_output_directory+'%s_condition_variances.csv' % (sub))
        temp_train1_frame.to_csv(current_working_dir+temp_output_directory+'%s_standard_train1_data.csv' %(sub))
        temp_test_frame.to_csv(current_working_dir+temp_output_directory+'%s_standard_test_data.csv' % (sub))

    
if __name__ == '__main__':
    main()
        
       




    
