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

BETWEEN_SUB_GRAPH_DIR = '\\graphs\\between\\'


SMALL_ABS_SEP  = 32
LARGE_ABS_SEP  = 44
ZERO_PEN       = 0
SMALL_PEN      = -1
LARGE_PEN      = -5
MULT_SMALL_PEN = -3
MULT_LARGE_PEN = -15

#all_e_subs = glob.glob('*_reach_train_output.csv')

for n in range(403, 450):
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
    all_dists_frame          = DataFrame()
    all_pokes_frame          = DataFrame()
    all_scores_frame         = DataFrame()
    all_opt_frame            = DataFrame()
    all_test_frames          = DataFrame()
    all_shifts_frame         = DataFrame()
    complete_shifts_frame    = DataFrame()
    all_mod_opt_frame        = DataFrame()


    #all_models_input = 'no'#input("Do you wish to merge the frames of shifts for each model? ('yes' or 'no'") 
    graph_input      = 'no'#input("Do you want to generate graphs? ('yes' or 'no')")
    #0: Condition-specific test var (CSTV) w/out loss aversion score (LA); 1: CSTV w/out LA; 1: CSTV w/ LA; 2: 
    #optimal_input    = 'all' #input("Which optimal model do you want to generate? ('CN', 'CL', 'RN', 'RL', 'TN', 'TL', or 'all')")
    

    # if subject_input == 'all':
    #   continue
    # elif isinstance(subject_input, int):
    #   all_subs = [literal_eval(subject_input)]
    # elif isinstance(subject_input, list) and isinstance(subject_input[0], int): 
    #   all_subs = subject_input
    # else:
    #   continue

    all_stat_frames = [all_vars_frame, all_dists_frame, all_pokes_frame, all_scores_frame, all_opt_frame, all_shifts_frame]

    #all_mod_opt_frame    = DataFrame() #stores ALL optimals, where each column specifies a condition and model, and each row is a subject
    #all_mod_shifts_frame = DataFrame()

    

    ##stores ALL x-discrepancies; 10 x (num models) columns, labeled with conditions and models; len(all_subs) rows, row for each subj
    opt_dict           = {}
    temp_opt_dict      = {}
    RN_opt_dict        = {}
    RL_opt_dict        = {}
    cond_avg_list      = []
    RN_aim_points      = []
    RL_aim_points      = []
    condition_list     = []
    sub_list           = []
    RN_x_point_list    = []
    RL_x_point_list    = []

    all_subs = [403]

    for sub in all_subs:  #'CN', 'CL','TN', 'TL'

        #all_sub_shifts_frame = DataFrame() #stores condition specific x-discrepancies; 10 columns, labeled with conditions and one model; len(all_subs) rows, row for each subj
        #all_sub_opt_frame    = DataFrame() #stores condition specific optimals for all subjects (rows) for one model: 10 columns, labeled with conditions and one model
        print "Subject number: " + str(sub)
        print "_________________________________"

        new_sub_list = [sub, sub, sub, sub, sub, sub, sub, sub, sub, sub] 
        sub_list.extend(new_sub_list) #adds 10 new copies of subject number to running subNum list
        condition_list.extend(CONDITION_LABELS) #adds another set of 10 conditions to condition list

        loss_aversion_score = get_LA_score(sub)

        temp_test_frame   = DataFrame() #stores standardized test data for one subject
        temp_stat_frames  = DataFrame() #stores stats for all conditions in train1, 2, or test for one subject 

        

        temp_output_directory = '\\graphs\\%s\\' % (sub)
        create_folder(temp_output_directory)

        temp_test_frame   = get_standard_test_frame(sub)
        
        temp_stat_frames  = get_stat_frames(temp_test_frame)
        #temp_stat_frames.append(temp_test_frame)

        #mean variance for each condition
        temp_vars         = temp_stat_frames[0]
       
        #test_x_var        = get_x_var(temp_test_frame)
        #test_y_var        = get_y_var(temp_test_frame)
        #mean variance for entire test
        #test_var          = np.mean([test_x_var, test_y_var])
        
        temp_train1_frame = get_standard_train1_frame(sub)
        train1_x_var      = get_x_var(temp_train1_frame)
        train1_y_var      = get_y_var(temp_train1_frame)
        #mean variance for entire training part 2
        train1_var        = np.mean([train1_x_var, train1_y_var])

        1/0

            

        n = 0
        
        for condition in CONDITION_LABELS: #CONDITION_LABELS

            print "Condition: " + condition
            print "___________________________________"



            #optimals_frame    = DataFrame() #stores optimal point for each condition for one subject
            #model_shift_frame = DataFrame() #stores x-discrepancies for one sub and one model; 10 columns, condition + model; 1 row
            

            # [sep, pen, rew] = get_condition_details(condition)
            # pen = abs(pen)
            # sep_frame     = temp_test_frame[temp_test_frame['absoluteSepDist'] == sep]
            # #subset of sep_frame including only trials with penalty value of pen
            # pen_sep_frame = sep_frame[sep_frame['penaltyVal'] == pen]
            cond_frame    = temp_test_frame[temp_test_frame['condition'] == n]

            cond_x        = cond_frame.standardPokePosX
            cond_avg_x    = cond_x.mean()
            
            
            cond_avg_list.append(cond_avg_x)


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
            
            n += 1

            # cond_var = temp_vars[condition].sum()
            # cond_vars.append(cond_var)
            
            #temp_points = [(-80, 0), (-60, 0), (-15, 0), (30, 0), (50, 0), (-70, 0), (-5, 0)]
            for optimal_input in ['RN', 'RL']:

                print "Model: " + optimal_input
                print "__________________________________"

                if optimal_input in ('CN', 'CL'):
                    temp_std = sqrt(temp_vars[condition].sum()) 
                elif optimal_input in ('RN', 'RL'):
                    temp_std = sqrt(train1_var)
                elif optimal_input in ('TN', 'TL'):
                    temp_std = sqrt(test_var)

                RN_aim_points = []
                RL_aim_points = []

                #print "getting ev array..."
                temp_ev_array  = get_EV_array(temp_std, condition, graph_input, optimal_input, loss_aversion_score, sub)

                #temp_ev_array.to_csv('%s_%s_%s_ev_array.csv' (sub, condition, optimal_input))

                #print "getting optimal point"
                #opt_dict[condition] = [get_optimal_aim_point(temp_ev_array)]

                optimal_aim_point = get_optimal_aim_point(temp_ev_array)

                

                if optimal_input == 'RN':
                    RN_x_point_list.append(optimal_aim_point[0])
                    RN_opt_dict[condition] = [optimal_aim_point]
                    RN_opt_dict['Model']   = [0]


                elif optimal_input == 'RL':
                    RL_x_point_list.append(optimal_aim_point[0]) 
                    RL_opt_dict[condition] = [optimal_aim_point]
                    RL_opt_dict['Model']  = [1]



                

                #print "generating EV landscape..."
                #create_EV_landscape(temp_ev_array, condition, temp_output_directory, optimal_input, sub, loss_aversion_score) #,opt_ev
                

                
                # # if n == 3:
                # #     1/0
                # # else: 
                # #     n += 1
        
        graph_by_val_sep_test_within(temp_test_frame, RN_opt_dict, temp_output_directory)
        graph_by_val_sep_test_within(temp_test_frame, RL_opt_dict, temp_output_directory)    



            #model_shift_frame = compute_model_fit(temp_test_frame, opt_dict, optimal_input)
     
            #print "Generating 2D Graphs including (1) avg aim points for each test condition and (2) optimal aim points, based on optimal input"
            
           
        
            # temp_stat_frames.append(optimals_frame)
            # temp_vars['subNum']         = sub
            # optimals_frame['subNum']    = sub
            # model_shift_frame['subNum'] = sub
            
            #all_vars_frame     = pd.concat([all_vars_frame, temp_vars])
            
            #all_sub_shifts_frame  = pd.concat([all_sub_shifts_frame, model_shift_frame])

                
            #mean_shifts = all_shifts_frame.mean()    

            #all_sub_opt_frame.to_csv('all_sub_%s_opt.csv' % (optimal_input))
            #all_sub_shifts_frame.to_csv('all_sub_%s_opt_shifts.csv' % (optimal_input))
            #mean_shifts.to_csv('%s_%s_opt_shifts.csv' % (subject_input, optimal_input))

        # all_sub_opt_frame     = pd.concat([all_sub_opt_frame, optimals_frame])
        # all_mod_shifts_frame  = pd.concat([all_mod_shifts_frame, all_sub_shifts_frame], axis = 1)

            
        # #mean_shifts = all_shifts_frame.mean()    

        # all_mod_opt_frame.to_csv('all_mod_opt.csv')
        # all_mod_shifts_frame.to_csv('all_mod_shifts.csv')

        #complete_shifts_frame = pd.merge(complete_shifts_frame, all_mod_shifts_frame)
    
           

    #     temp_opt_dict['SubNum']    = sub_list
    #     temp_opt_dict['Condition'] = condition_list
    #     temp_opt_dict['AvgX']      = cond_avg_list
    #     temp_opt_dict['NoLossX']   = RN_x_point_list
    #     temp_opt_dict['LossX']     = RL_x_point_list
    #     temp_opt_frame             = pd.DataFrame(dict([(k,Series(v)) for k,v in temp_opt_dict.iteritems()]))
    #     temp_opt_frame.to_csv('temp_avgX_train_modelsX_to_sub_%s.csv' % (sub))
    #     graph_var_by_cond_between(all_vars_frame, BETWEEN_SUB_GRAPH_DIR)
    
    # opt_dict['SubNum']    = sub_list
    # opt_dict['Condition'] = condition_list
    # opt_dict['AvgX']      = cond_avg_list
    # opt_dict['NoLossX']   = RN_x_point_list
    # opt_dict['LossX']     = RL_x_point_list
    # opt_frame             = pd.DataFrame(dict([(k,Series(v)) for k,v in opt_dict.iteritems()]))
    # opt_frame.to_csv('avgX_modelsX.csv')


    
if __name__ == '__main__':
    main()
        
       




    
