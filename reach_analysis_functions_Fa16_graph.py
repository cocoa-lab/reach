import numpy as np
import pandas as pd 
import scipy as sp 
import os 
import errno
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
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
# import statsmodels.api as sm
from operator import itemgetter

from reach_analysis_constants_Fa16 import *
 
# rcParams.update({'figure.autolayout': True})
#style.use('fivethirtyeight')
 

     
def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def get_LA_score(sub):
    LA_score_frame = pd.read_csv(current_working_dir + '/loss_aversion/All_lambdas.csv')
    LA_score       = LA_score_frame[LA_score_frame['subNum'] == sub].lambdas.mean()
    return LA_score

def get_optimal_aim_point(ev_array):
    opt_ev  = get_opt_point_ev(ev_array)
    return opt_ev[0]


#computes the x_distance between the actual avg and model-predicted aim points for each combination of penalty values and separation distances
#returns these distances as a 1-row dataframe with columns labeled according to penalty value, separation distance, and model type
def compute_model_fit(test_frame, optimal_dict, optimal_input):

    cl_code = 0
    abs_seps = [SMALL_ABS_SEP, LARGE_ABS_SEP]
    pen_vals = [ZERO_PEN, SMALL_PEN, MULT_SMALL_PEN, LARGE_PEN, MULT_LARGE_PEN]
    dis_dict = {}
    
    for sep in abs_seps:
        for pen in pen_vals:

            #subset of test_frame including only trials with separation distance of sep
            sep_frame     = test_frame[test_frame['absoluteSepDist'] == sep]
            #subset of sep_frame including only trials with penalty value of pen
            pen_sep_frame = sep_frame[sep_frame['penaltyVal'] == pen]
            #average standardized x position from pen_sep_frame
            avg_x         = pen_sep_frame.standardPokePosX.mean()

            #(x, y) position of optimal point for this separation distance of sep and penalty value of pen; see CONDITION_LABELS in constants file
            #optimal_dict[LABEL] yields a list containing a single (x,y) ordered pair
            model_point   = optimal_dict[CONDITION_LABELS[cl_code]][0]
            model_x       = model_point[0]

            dist = avg_x - model_x

            dis_dict[CONDITION_LABELS[cl_code] + '_' + optimal_input] = [dist]

            cl_code += 1
   
    dist_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in dis_dict.iteritems()]))

    return dist_frame

#takes a subject's standardized frame and generates qq-plots comparing all x and y positions to a normal distribution
def q_q_plot(sub_frame):
 
    axes = []
 
    for c in CONDITION_CODES:
 
        x = sub_frame[sub_frame['condition'] == c].standardPokePosX
        y = sub_frame[sub_frame['condition'] == c].standardPokePosY
 
        axX = sm.qqplot(x, fit = True, line = '45')
        axY = sm.qqplot(y, fit = True, line = '45')
         
        axes.append((ax1, ax2))
     
    fig, axes = plt.subplots(10,2, sharex='col', sharey='row')


#takes an array of (aim_point, expected value) pairs and the condition (i.e., string of sep dist, pen val) for which this array was generated
#generates a 3-D graph where each x,y coordinate is associated with some expected value plotted on z axis, graphs saved in output directory
def create_EV_landscape(ev_array, condition, output_dir, optimal_input, sub, LA_score):
    
    #EVs    = [item[1] for item in ev_array]
    #points = [item[0] for item in ev_array]

    [temp_horiz_min, temp_horiz_max] = get_horiz_min_max(condition)
    [temp_vert_min, temp_vert_max]   = get_vert_min_max(condition)

    if sub == 403:
        temp_horiz_max = 40
        temp_horiz_min = -70
        temp_vert_max  = 55
        temp_vert_min  = -55

    X = np.arange(temp_horiz_min, temp_horiz_max, SIM_GRID_GRAN)
    Y = np.arange(temp_vert_min, temp_vert_max, SIM_GRID_GRAN)

    # X = np.array(X)
    # Y = np.array(Y)

    X, Y = np.meshgrid(X, Y) #X.astype(np.int8), Y.astype(np.int8)

    temp_grid_width  = (abs(temp_horiz_min) + temp_horiz_max) * 1/SIM_GRID_GRAN
    temp_grid_height = temp_grid_width

    Z = np.zeros([temp_grid_width, temp_grid_height]) 

    #n = 0 

    #print np.shape(f)
    #print np.shape(ev_array)
    for i in ev_array:

        x = i[0][0]
        y = i[0][1]

        x += abs(temp_horiz_min)
        y += abs(temp_vert_min)

        #print n

        Z[y][x] = i[1]
        #n += 1


    fig = plt.figure()
    ax  = fig.gca(projection='3d')


    cond  = get_condition_details(condition)

    z_min = cond[1]
    z_max = cond[2]

    if optimal_input in LOSS_AVERSION_MODELS:
        z_min = cond[1] * abs(LA_score)

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=mpl.cm.Spectral, zorder = 1) #, alpha = 0.3
    
    if z_min == 0:
        z_min = -0.5
    else:
        z_min = z_min

    # temp_opt_point = opt_point_ev_pair[0]
    # opt_x = temp_opt_point[0]
    # opt_y = temp_opt_point[1]
    # opt_z = opt_point_ev_pair[1]

    #ax.scatter(opt_y, opt_x, opt_z, c = 'k', s = 75, marker = '*', zorder = 2)

    cset = ax.contourf(X, Y, Z, offset = z_min, cmap=mpl.cm.Spectral) #levels = levels
    # cset = ax.contourf(X, Y, Z, zdir='x', offset=temp_horiz_min, cmap=mpl.cm.Spectral)
    # cset = ax.contourf(X, Y, Z, zdir='y', offset=SIM_GRID_VERT_MAX, cmap=mpl.cm.Spectral)

    
    # filter out extra ticks that exceed data limits
    ax.set_zticks(filter(lambda x: z_min <= x <= z_max, ax.get_zticks()))
    ax.set_zlim(z_min, z_max)
    ax.set_zlabel('Z')
    ax.set_xlim(temp_horiz_min, temp_horiz_max)
    ax.set_xlabel('X')
    ax.set_ylim(temp_vert_min, temp_vert_max)
    ax.set_ylabel('Y')

    # ax.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    plt.savefig(current_working_dir + output_dir + optimal_input + condition + '_'  + '_3D_EV_landscape.pdf', bbox_inches = 'tight')
    
    #plt.show()
    plt.close()

#determines the maximum and minimum x_position of the simulated points; with min based on sep_dist
def get_horiz_min_max(condition):
    
    cond = get_condition_details(condition)

    if cond[0] == LARGE_ABS_SEP:
        horiz_min = SIM_GRID_HORIZ_MIN_LARGE
    else:
        horiz_min = SIM_GRID_HORIZ_MIN_SMALL

    horiz_max = SIM_GRID_HORIZ_MAX

    return [horiz_min, horiz_max]

#determines the max and min y_position of the simulated points, based on sep dist
def get_vert_min_max(condition):

    cond = get_condition_details(condition)

    if cond[0] == LARGE_ABS_SEP:
        vert_min = SIM_GRID_VERT_MIN_LARGE
        vert_max = SIM_GRID_VERT_MAX_LARGE
    else:
        vert_min = SIM_GRID_VERT_MIN_SMALL
        vert_max = SIM_GRID_VERT_MAX_SMALL

    return [vert_min, vert_max]

#takes a standard deviation (float) and a condition (string of the form 'abs(sepdist),abs(penaltyVal)', e.g., '32,0', '44,15', etc.;
#iterates through a grid of possible aim points and computes the EV for each aim point
#returns the result as an array of tuples containing aimpoints and EVs (see get_optimal_aim_point() RME)
def get_EV_array(standard_deviation, condition, graph_input, optimal_input, LA_score, sub):
     
    EV_by_aimpoint = []
    
    #get L, R, top, and bottom bounds of simulated grid
    [temp_horiz_min, temp_horiz_max] = get_horiz_min_max(condition)
    [temp_vert_min, temp_vert_max]   = get_vert_min_max(condition)

    if sub == 403:
        temp_horiz_max = 40
        temp_horiz_min = -70
        temp_vert_max  = 55
        temp_vert_min  = -55

    y_range = np.arange(temp_vert_min, temp_vert_max, SIM_GRID_GRAN)
    
     
    for x in np.arange(temp_horiz_min, temp_horiz_max, SIM_GRID_GRAN):
        for y in y_range: #***when not generating 3D EV graphs, need not check nonzero y

     
            x_sample = stats.norm.rvs(loc = x, scale = standard_deviation, size = SIM_POKE_NUM)
            y_sample = stats.norm.rvs(loc = y, scale = standard_deviation, size = SIM_POKE_NUM)

            total_earnings = 0
            earnings_list  = []

            for n in range(SIM_POKE_NUM):#i, j in zip(x_sample, y_sample):

                    earned = get_poke_earning((x_sample[n], y_sample[n]), condition, optimal_input, LA_score)
                    
                    total_earnings += earned

                    earnings_list.append(earned)

            EV = float(total_earnings) / SIM_POKE_NUM

            EV_by_aimpoint.append(((x, y), EV))
    
    return EV_by_aimpoint

#takes array of tuples, such that tuple[0] == an aimpoint (e.g., (32, 0)) and tuple[1] == an EV (e.g., .80); returns the aimpoint associated with the greatest EV, i.e., the optimal aimpoint
def get_opt_point_ev(ev_array):

    ev_array = sorted(ev_array,key=itemgetter(1))

    optimal_aim_point = ev_array[-1][0]
    optimal_ev = ev_array[-1][1]
    

    return [optimal_aim_point, optimal_ev]
 
#pass condition string, as in the column titles in the various stats dataframes (e.g., "32,1", "44,15", etc.) #returns list of condition details as integers
def get_condition_details(condition):
 
    condition_tuple = literal_eval(condition)

    sep = condition_tuple[0]
    pen = condition_tuple[1]

    if -pen == MULT_SMALL_PEN or -pen == MULT_LARGE_PEN:
        rew = MULT_REWARD
    else:
        rew = REWARD

    return [sep, -pen, rew]
 
#takes a position (x,y) and condition in the string (see get_condition_details() RME)
def get_poke_earning(position, condition, optimal_input, LA_score):
 
    [sep, pen, rew] = get_condition_details(condition)

    

    if optimal_input in LOSS_AVERSION_MODELS:
        pen *= abs(LA_score)
    

    dist_from_targ = distance(position, TARG_POS)
    
    #determine location of penalty center by separation distance
    if sep == LARGE_ABS_SEP:
        dist_from_pen = distance(position, PEN_POS_LARGE)
    else:
        dist_from_pen = distance(position, PEN_POS_SMALL)
    
    #determine whether the poke hit the target/penalty by distance from center
    if dist_from_pen <= RADIUS:
        pen_poke = True
    else:
        pen_poke = False
 
    if dist_from_targ <= RADIUS:
        targ_poke = True
    else:
        targ_poke = False
 
    #determine the the amount earned based on the regions hit
    if pen_poke and targ_poke:
        earning = pen + rew
    elif pen_poke:
        earning = pen
    elif targ_poke:
        earning = rew
    else:
        earning = 0
 
    return earning
 
#takes frame of test data, computes levene stat (and significance thereof) of difference between L & R x_variability and L & R y_variability
#stores p_values of these levene stats in dataframes and returns a list of these frames
def get_LR_lev_frames(test_frame):
 
    test_frame = test_frame.dropna()
 
    #dictionary for storing lev stats of L and R X_variability for each sep dist magnitude and pen value
    LR_x_lev_dict = {'32,0': [], '44,0': [],  '32,1': [],
      '44,1': [],  '32,3': [],  '44,3': [], 
      '32,5': [],  '44,5': [],  '32,15': [],
      '44,15': []}
    #dictionary for storing lev stats of L and R Y_variability for each sep dist magnitude and pen value
    LR_y_lev_dict = {'32,0': [], '44,0': [],  '32,1': [],
      '44,1': [],  '32,3': [],  '44,3': [], 
      '32,5': [],  '44,5': [],  '32,15': [],
      '44,15': []}
 
    for sep in SEP_DIST_MAGS:
        left_sep_frame  = test_frame[test_frame['sepDist'] == sep]
        right_sep_frame = test_frame[test_frame['sepDist'] == -sep] 
        for val in PEN_VALS:
            right_pen_frame = right_sep_frame[right_sep_frame['penaltyVal'] == -val]
            left_pen_frame  = left_sep_frame[left_sep_frame['penaltyVal'] == -val]
 
            left_x = left_pen_frame.standardPokePosX
            left_y = left_pen_frame.standardPokePosY
 
            right_x = right_pen_frame.standardPokePosX
            right_y = right_pen_frame.standardPokePosY
 
            x_lev = stats.levene(left_x, right_x)
            y_lev = stats.levene(left_y, right_y)
 
            dict_label = '%s,%s' %(sep, val)
 
            LR_x_lev_dict[dict_label].append(x_lev[1])
            LR_y_lev_dict[dict_label].append(y_lev[1])
 
    LR_x_lev_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in LR_x_lev_dict.iteritems()]))
    LR_y_lev_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in LR_y_lev_dict.iteritems()]))
     
    return [LR_x_lev_frame, LR_y_lev_frame]
 
#takes in a subject's standardized test dataframe, 
#computes mean variance, lev_stat  (and signif. thereof) of x & y vars, total score, and mean dist from target for each of 20 conditions
#creates and returns list of 5, 1x20 dataframes from these above values
def get_stat_frames(test_frame):
 
    na_frame   = test_frame
    test_frame = test_frame.dropna()
     
    #dictionary for storing levene stats of x&y var for each condition
    # lev_dict = {'32,0': [], '-32,0': [], '44,0': [], '-44,0': [], '32,1': [], '-32,1': [],
    #   '44,1': [], '-44,1': [], '32,3': [], '-32,3': [], '44,3': [], '-44,3': [],
    #   '32,5': [], '-32,5': [], '44,5': [], '-44,5': [], '32,15': [], '-32,15': [], 
    #   '44,15': [], '-44,15': []}
    #dictionary for storing means of x&y var for each condition
    mean_var_dict = {'32,0': [], '44,0': [],  '32,1': [],
      '44,1': [],  '32,3': [],  '44,3': [], 
      '32,5': [],  '44,5': [],  '32,15': [],
      '44,15': []}
    #dictionary for storing mean poke distance from target (pix) for each condition
    mean_dist_dict = {'32,0': [], '44,0': [],  '32,1': [],
      '44,1': [],  '32,3': [],  '44,3': [], 
      '32,5': [],  '44,5': [],  '32,15': [],
      '44,15': []}
    #dictionary for storing total score for each condition
    score_dict = {'32,0': [], '44,0': [],  '32,1': [],
      '44,1': [],  '32,3': [],  '44,3': [], 
      '32,5': [],  '44,5': [],  '32,15': [],
      '44,15': []}
    #dictionary for storing mean x and mean y poke position for each condition
    mean_poke_dict = {'32,0': [], '44,0': [],  '32,1': [],
      '44,1': [],  '32,3': [],  '44,3': [], 
      '32,5': [],  '44,5': [],  '32,15': [],
      '44,15': []}
     
    for sep in SEP_DIST_MAGS:

        temp_dist_frame = test_frame[test_frame['sepDist'] == sep]
        temp_na_D_frame = na_frame[na_frame['sepDist'] == sep]

        for val in PEN_VALS:

            temp_val_frame  = temp_dist_frame[temp_dist_frame['penaltyVal'] == -val]
            temp_na_V_frame = temp_na_D_frame[temp_na_D_frame['penaltyVal'] == -val]
             
            x = temp_val_frame.standardPokePosX
            y = temp_val_frame.standardPokePosY
 
            mean_x = np.mean(x)
            mean_y = np.mean(y)
            mean_poke = [mean_x, mean_y]
 
            # lev_stat = stats.levene(x, y)
            
            x_var = np.nanvar(x) 
            y_var = np.nanvar(y)
            mean_var = np.mean([x_var, y_var])
 
            dists = temp_val_frame.targDist
            mean_dist = np.mean(dists)
 
 
            scores = temp_na_V_frame.score
            total_score = sum(scores)
 
 
            dict_label = '%s,%s' %(sep, val)
 
            # lev_dict[dict_label].append(lev_stat[1])
            mean_var_dict[dict_label].append(mean_var)
            mean_dist_dict[dict_label].append(mean_dist)
            score_dict[dict_label].append(total_score)
            mean_poke_dict[dict_label].append(mean_poke)
 
             
 
    # lev_stat_frame  = pd.DataFrame(dict([(k,Series(v)) for k,v in lev_dict.iteritems()]))
    mean_var_frame  = pd.DataFrame(dict([(k,Series(v)) for k,v in mean_var_dict.iteritems()]))
    mean_dist_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in mean_dist_dict.iteritems()]))
    mean_poke_frame = pd.DataFrame(dict([(k,Series(v)) for k,v in mean_poke_dict.iteritems()]))
    score_frame     = pd.DataFrame(dict([(k,Series(v)) for k,v in score_dict.iteritems()]))
 
    return [mean_var_frame, mean_dist_frame, mean_poke_frame, score_frame]
 
#takes a string of desired folder name preceded by parent folder name (e.g., '\\PARENT\\CHILD\\'))
#tries to create this folder 
#does nothing if folder was already created
def create_folder(folder_names):
    path = current_working_dir  + folder_names
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
 
#takes dataframe returned by standard_train1_frame
#returns variance of poke x-position 
def get_x_var(standard_frame):
 
    return np.nanvar(standard_frame.standardPokePosX)
 
#takes dataframe returned by standard_train1_frame
#returns variance of poke y-position 
def get_y_var(standard_frame):
 
    return np.nanvar(standard_frame.standardPokePosY)
 
#creates dataframe from TRAINING PART 1 output file
#adds two columns to dataframe (standardized poke position and absolute value of sep dists)
#returns modded dataframe
def get_standard_train1_frame(subject_number):
 
    train1_frame  = pd.read_csv('%s%s_reach_train1_output.csv' % (input_dir, subject_number), index_col=0)
 
    #standardized poke positions factor out the jittered position of the target   
    standard_pokes_x = []
    standard_pokes_y = []
 
    #absolute values of the standardized poke positions
    absolute_pokes_x = [] 
    absolute_pokes_y = []
 
    for n in range(0, len(train1_frame.index)):
         
         
        temp_targ_pos = literal_eval(train1_frame.iloc[n]['aimDotPos'])
        temp_poke_pos = train1_frame.iloc[n]['pokePos']
 
        if pd.isnull(temp_poke_pos): #false if temp_poke_pos is a position tuple-like string (i.e., if the poke was successful)
            standard_poke_pos_x = float('nan')
            standard_poke_pos_y = float('nan')
            abs_poke_pos_y      = float('nan')
            abs_poke_pos_x      = float('nan')
 
        else:
            temp_poke_pos = literal_eval(temp_poke_pos) 
             
            standard_poke_pos_x = temp_poke_pos[0] - temp_targ_pos[0] 
            standard_poke_pos_y = temp_poke_pos[1] - temp_targ_pos[1]
 
            abs_poke_pos_x      = abs(standard_poke_pos_x)
            abs_poke_pos_y      = standard_poke_pos_y

        if standard_poke_pos_x < OUT_X_MIN or standard_poke_pos_x > OUT_X_MAX:
            standard_poke_pos_x = float('nan')
            standard_poke_pos_y = float('nan')

        if standard_poke_pos_y < OUT_Y_MIN or standard_poke_pos_y > OUT_Y_MAX:
            standard_poke_pos_y = float('nan')
            standard_poke_pos_x = float('nan')
       
        standard_pokes_x.append(standard_poke_pos_x)
        standard_pokes_y.append(standard_poke_pos_y)
        absolute_pokes_x.append(abs_poke_pos_x)
        absolute_pokes_y.append(abs_poke_pos_y)
     
 
    train1_frame['standardPokePosX'] = standard_pokes_x
    train1_frame['standardPokePosY'] = standard_pokes_y
 
    train1_frame['absolutePokePosX'] = absolute_pokes_x
    train1_frame['absolutePokePosY'] = absolute_pokes_y
 
    return train1_frame
 
 
#creates dataframe from TRAINING PART 2 output file
#adds two columns to dataframe (standardized poke position and absolute value of sep dists)
#returns modded dataframe
def get_standard_train2_frame(subject_number):

    train2_frame  = pd.read_csv('%s%s_reach_train2_output.csv' % (input_dir, subject_number), index_col=0)
       
    #standardized poke positions factor out the jittered position of the target   
    standard_pokes_x = []
    standard_pokes_y = []
    #absolute values of the standardized poke positions
    absolute_pokes_x = [] 
    absolute_pokes_y = []
    absolute_seps    = []
    too_slow_bools   = []
    multiplier_bools = []
 
    for n in range(0, len(train2_frame.index)):
         
        temp_targ_pos = literal_eval(train2_frame.iloc[n]['targetPos'])
        temp_poke_pos = train2_frame.iloc[n]['pokePos']
        temp_sep_dist = train2_frame.iloc[n]['sepDist']
        
 
        if pd.isnull(temp_poke_pos): #false if temp_poke_pos is a position tuple-like string (i.e., if the poke was successful)
            standard_poke_pos_x = float('nan')
            standard_poke_pos_y = float('nan')
            abs_poke_pos_y      = float('nan')
            abs_poke_pos_x      = float('nan')
            temp_too_slow       = 1
 
        else:
            temp_poke_pos       = literal_eval(temp_poke_pos)
            standard_poke_pos_x = temp_poke_pos[0] - temp_targ_pos[0] 
            standard_poke_pos_y = temp_poke_pos[1] - temp_targ_pos[1]
            abs_poke_pos_x      = abs(standard_poke_pos_x)
            abs_poke_pos_y      = standard_poke_pos_y
            temp_too_slow       = 0
 
            #if the target was drawn left of the penalty, then reflect the shifted poke position over the y_axis, otherwise do nothing
            if train2_frame.iloc[n]['sepDist'] > 0:
               standard_poke_pos_x = abs_poke_pos_x
         
        if standard_poke_pos_x < OUT_X_MIN or standard_poke_pos_x > OUT_X_MAX:
            standard_poke_pos_x = float('nan')
            standard_poke_pos_y = float('nan')

        if standard_poke_pos_y < OUT_Y_MIN or standard_poke_pos_y > OUT_Y_MAX:
            standard_poke_pos_y = float('nan')
            standard_poke_pos_x = float('nan')
 
        abs_sep = abs(temp_sep_dist)
        
        standard_pokes_x.append(standard_poke_pos_x)
        standard_pokes_y.append(standard_poke_pos_y)
        absolute_pokes_x.append(abs_poke_pos_x)
        absolute_pokes_y.append(abs_poke_pos_y)
        absolute_seps.append(abs_sep)
        too_slow_bools.append(temp_too_slow)

    
    train2_frame['tooSlow']          = too_slow_bools
    train2_frame['standardPokePosX'] = standard_pokes_x
    train2_frame['standardPokePosY'] = standard_pokes_y
    train2_frame['absolutePokePosX'] = absolute_pokes_x
    train2_frame['absolutePokePosY'] = absolute_pokes_y
    train2_frame['absoluteSepDist']  = absolute_seps
    
    conditions = [] 
    multiplier = 0

    for n in range(0, len(train2_frame.index)):

        if abs(train2_frame.iloc[n]['absoluteSepDist'])   == SMALL_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == ZERO_PEN:
            condition  = ZERO_SMALL
            multiplier = 0
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == ZERO_PEN:
            condition  = ZERO_LARGE
            multiplier = 0
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == SMALL_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == SMALL_PEN:
            condition  = SMALL_SMALL
            multiplier = 0
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == SMALL_PEN:
            condition  = SMALL_LARGE
            multiplier = 0
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == SMALL_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == MULT_SMALL_PEN:
            multiplier = 1
            condition  = MULT_SMALL_SMALL
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == MULT_SMALL_PEN:
            multiplier = 1
            condition  = MULT_SMALL_LARGE
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == SMALL_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == LARGE_PEN:
            condition = LARGE_SMALL
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == LARGE_PEN:
            condition = LARGE_LARGE
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == SMALL_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == MULT_LARGE_PEN:
            multiplier = 1
            condition  = MULT_LARGE_SMALL  
        elif abs(train2_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and train2_frame.iloc[n]['penaltyVal'] == MULT_LARGE_PEN:
            multiplier = 1
            condition  = MULT_LARGE_LARGE 
        else:
            multiplier = 0
            condition  = 0

        conditions.append(condition)
        multiplier_bools.append(multiplier)
    
    train2_frame['condition']        = conditions
    train2_frame['multiplierTrial']  = multiplier_bools

    return train2_frame

 
#creates dataframe from TEST output file
#adds two columns to dataframe (standardized poke position and absolute value of sep dists)
#returns modded dataframe
def get_standard_test_frame(subject_number):
 
    test_frame    = pd.read_csv('%s%s_reach_test_output.csv' % (input_dir, subject_number), index_col=0)
       
    #standardized poke positions factor out the jittered position of the target   
    standard_pokes_x = []
    standard_pokes_y = []
    conditions       = []
    #absolute values of the standardized poke positions
    absolute_pokes_x = [] 
    absolute_pokes_y = []
    absolute_seps    = []
    too_slow_bools   = []
    multiplier_bools = []
    loss_gain_ratios = []
 
    for n in range(0, len(test_frame.index)):
         
        temp_targ_pos = literal_eval(test_frame.iloc[n]['targetPos'])
        temp_poke_pos = test_frame.iloc[n]['pokePos']
        temp_sep_dist = test_frame.iloc[n]['sepDist']

        # if test_frame.iloc[n]['penaltyVal'] in [-1, -3]:
        #     loss_gain_ratios.append(ONE_ONE)
        # elif test_frame.iloc[n]['penaltyVal'] in [-5, -15]:
        #     loss_gain_ratios.append(THREE_ONE)
        # else:
        #     loss_gain_ratios.append(0)

        # if test_frame.iloc[n]['penaltyVal'] in [-3, -15]:
        #     loss_gain_ratios.append(MULTIPLIER)
        # else:
        #     multiplier_bools.append(NON_MULTIPLIER)

        if test_frame.iloc[n]['pokeTime'] >= 1:
            too_slow_bools.append(1)
        else:
            too_slow_bools.append(0)
 
        if pd.isnull(temp_poke_pos): #false if temp_poke_pos is a position tuple-like string (i.e., if the poke was successful)
            standard_poke_pos_x = float('nan')
            standard_poke_pos_y = float('nan')
            abs_poke_pos_y      = float('nan')
            abs_poke_pos_x      = float('nan')
            
 
        else:
            temp_poke_pos       = literal_eval(temp_poke_pos)
            standard_poke_pos_x = temp_poke_pos[0] - temp_targ_pos[0] 
            standard_poke_pos_y = temp_poke_pos[1] - temp_targ_pos[1]
            abs_poke_pos_x      = abs(standard_poke_pos_x)
            abs_poke_pos_y      = standard_poke_pos_y
            
 
            #if the target was drawn left of the penalty, then reflect the shifted poke position over the y_axis, otherwise do nothing
            if test_frame.iloc[n]['sepDist'] > 0:
               standard_poke_pos_x = -standard_poke_pos_x
         
        # if standard_poke_pos_x < OUT_X_MIN or standard_poke_pos_x > OUT_X_MAX:
        #     standard_poke_pos_x = float('nan')
        #     standard_poke_pos_y = float('nan')

        # if standard_poke_pos_y < OUT_Y_MIN or standard_poke_pos_y > OUT_Y_MAX:
        #     standard_poke_pos_y = float('nan')
        #     standard_poke_pos_x = float('nan')


 
        abs_sep = abs(temp_sep_dist)
        
        standard_pokes_x.append(standard_poke_pos_x)
        standard_pokes_y.append(standard_poke_pos_y)
        absolute_pokes_x.append(abs_poke_pos_x)
        absolute_pokes_y.append(abs_poke_pos_y)
        absolute_seps.append(abs_sep)
        #too_slow_bools.append(too_slow)

    

    # test_frame['multiplier']       = multiplier_bools
    # test_frame['loss_gain_ratio']  = loss_gain_ratios
    test_frame['tooSlow']          = too_slow_bools
    test_frame['standardPokePosX'] = standard_pokes_x
    test_frame['standardPokePosY'] = standard_pokes_y
    test_frame['absolutePokePosX'] = absolute_pokes_x
    test_frame['absolutePokePosY'] = absolute_pokes_y
    test_frame['absoluteSepDist']  = absolute_seps
    
    #conditions = [] 

    for n in range(0, len(test_frame.index)):

        if abs(test_frame.iloc[n]['absoluteSepDist'])   == SMALL_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == ZERO_PEN:
            condition  = ZERO_SMALL
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == ZERO_PEN:
            condition  = ZERO_LARGE
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == SMALL_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == SMALL_PEN:
            condition  = SMALL_SMALL
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == SMALL_PEN:
            condition  = SMALL_LARGE
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == SMALL_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == MULT_SMALL_PEN:
            condition  = MULT_SMALL_SMALL
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == MULT_SMALL_PEN:
            condition  = MULT_SMALL_LARGE
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == SMALL_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == LARGE_PEN:
            condition = LARGE_SMALL
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == LARGE_PEN:
            condition = LARGE_LARGE
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == SMALL_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == MULT_LARGE_PEN:
            condition  = MULT_LARGE_SMALL  
        elif abs(test_frame.iloc[n]['absoluteSepDist']) == LARGE_ABS_SEP and test_frame.iloc[n]['penaltyVal'] == MULT_LARGE_PEN:
            condition  = MULT_LARGE_LARGE 
        

        conditions.append(condition)
    
    test_frame['condition']        = conditions

    #for sake of analysis, throw out all trials where poke occurred after 1s
    test_frame = test_frame[test_frame['tooSlow'] == 0]

    return test_frame
 
#takes a dataframe returned by get_standard_test_frame(), a positive separation distance constant, and a subject number
#creates a graph of all standardized pokes by the given subject during the test in trials with the given separation distance 
#saves graphs in ...\\reach\\graphs\\S where S is the given subject number
#filename specifies the given separation distance and dataframe type which is test for this function
def graph_by_sep_test_within(test_frame, separation_distance, output_dir):
 
 
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
    avg_mark = plt.Circle((avg_x, avg_y), 1,color='b',fill=False)
 
 
    target  = plt.Circle((0,0), RADIUS, color='g',fill=False)
    penalty = plt.Circle((-separation_distance,0), RADIUS, color='r', fill=False) 
     
    plt.gcf().gca().add_artist(target)
    plt.gcf().gca().add_artist(penalty)
    plt.gcf().gca().add_artist(avg_mark)
    plt.savefig(current_working_dir + output_dir + 'sep' + str(separation_distance) + '_test.pdf', bbox_inches='tight')
    plt.close(fig)
 

#takes a dataframe returned by get_standard_test_frame(), a frame of optimal aim points for each condition, and an output directory all specific to a subject
#creates a graph of all standardized pokes by the given subject during the test in trials with the given penalty value
#plots the optimal (pink star) and average aim point (yellow dot) for the subject and condition 
#saves graphs in .../reach/graphs/S where S is the given subject number
#also computes and returns a dataframe of the cartesian distance between the optimal and average aim points for each condition
def graph_by_val_sep_test_within(test_frame, optimal_dict, output_dir):

    cl_code = 0
    abs_seps = [SMALL_ABS_SEP, LARGE_ABS_SEP]
    pen_vals = [ZERO_PEN, SMALL_PEN, MULT_SMALL_PEN, LARGE_PEN,  MULT_LARGE_PEN]

    fig, ((ax1,ax6), (ax2, ax7), (ax3,ax8), (ax4, ax9), (ax5, ax10)) = plt.subplots(5,2, sharex='col', sharey='row')

    axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10]

    
    
    for sep in abs_seps:
        for pen in pen_vals:

            #subset of test_frame including only trials with separation distance of sep
            sep_frame     = test_frame[test_frame['absoluteSepDist'] == sep]
            #subset of sep_frame including only trials with penalty value of pen
            pen_sep_frame = sep_frame[sep_frame['penaltyVal'] == pen]
            x             = pen_sep_frame.standardPokePosX
            y             = pen_sep_frame.standardPokePosY
            #average standardized x position from pen_sep_frame
            avg_x         = x.mean()
            avg_y         = y.mean()

            #(x, y) position of optimal point for this separation distance of sep and penalty value of pen; see CONDITION_LABELS in constants file
            #optimal_dict[LABEL] yields a list containing a single (x,y) ordered pair
            model_point       = optimal_dict[CONDITION_LABELS[cl_code]][0]
            model_x           = model_point[0]
            model_y           = model_point[1]


            axes[cl_code].plot(x, y, "o", color='black', zorder = 1)

            axes[cl_code].plot((model_x), (model_y), '*', color = 'm', zorder = 2)

            avg_mark = plt.Circle((avg_x, avg_y), 1 ,color='b',fill=False)
            target   = plt.Circle((0,0),  RADIUS,color='g',fill=False)
            # axes[cl_code.plot((avg_x), (avg_y), 'o', color = 'y')
            penalty  = plt.Circle((-sep,0), RADIUS, color='r', fill=False) 
            axes[cl_code].add_artist(target)
            axes[cl_code].add_artist(penalty)
            axes[cl_code].add_artist(avg_mark)
            axes[cl_code].set_title(CONDITION_LABELS[cl_code])

            axes[cl_code].set_xlim([-100, 100])
            axes[cl_code].set_ylim([-50, 50])

            cl_code += 1

    fig.set_size_inches((9, 12))
    if optimal_dict['Model'] == [0]:
        plt.savefig(current_working_dir + output_dir + 'RN_val_sep_test.pdf')
    elif optimal_dict['Model'] == [1]:
        plt.savefig(current_working_dir + output_dir + 'RL_val_sep_test.pdf')
    plt.close(fig)

 
 
#takes a frame of mean variances with condition columns and subject rows
#averages variances across subjects and plots graph of average variance for each condition
#error bars represent standard deviation of variances for each condition
def graph_var_by_cond_between(var_frame, output_dir):
 
    ax  = plt.gca()
    fig = plt.gcf()
    ax.set_xlim()
 
 
    cols  = var_frame.columns.tolist()
    order = [0, 1, 3, 4, 2, 5, 6, 8, 9, 7] 
    cols = [cols[i] for i in order]
 
    var_frame = var_frame[cols]
 
    num_subs  = len(var_frame.index)
 
    mean_vars = var_frame.mean()
    sem_vars  = var_frame.sem()
 
    mean_vars.plot(kind = 'bar', yerr = sem_vars)
 
    plt.savefig(current_working_dir + output_dir + 'cond_var_graph.pdf', bbox_inches = 'tight')
 
    plt.close(fig)
 
 
def graph_releaseTime_by_cond_within(test_frame, output_dir):
    ax  = plt.gca()
    fig = plt.gcf()
    ax.set_xlim()
 
    frame = test_frame.groupby(['penaltyVal', 'absoluteSepDist']).releaseTime.mean()
    err   = test_frame.groupby(['penaltyVal', 'absoluteSepDist']).releaseTime.sem()
 
    frame.plot(kind = 'bar', yerr = err)
 
    plt.savefig(current_working_dir + output_dir + 'release_time_by_cond', bbox_inches = 'tight')
 
    plt.close(fig)
 
def graph_pokeTime_by_cond_within(test_frame, output_dir):
 
    ax  = plt.gca()
    fig = plt.gcf()
    ax.set_xlim()
 
    frame = test_frame.groupby(['penaltyVal', 'absoluteSepDist']).pokeTime.mean()
    err   = test_frame.groupby(['penaltyVal', 'absoluteSepDist']).pokeTime.sem()
 
    frame.plot(kind = 'bar', yerr = err)
 
    plt.savefig(current_working_dir + output_dir + 'poke_time_by_cond', bbox_inches = 'tight')
 
    plt.close(fig)