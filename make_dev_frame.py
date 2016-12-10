import pandas as pd
import os
from pandas import Series, DataFrame
from math import sqrt
all_subs = []

for n in range(403, 550):
    try: 
        temp_frame = pd.read_csv('model_estimates/%s_N_model_aim_estimates.csv' % (n), index_col = 0)
        if n != 999:
            all_subs.append(n)
    except: 
        continue        

models = ['N', 'Y']
seps   = [32, 44]
pens   = [0, 1, 3, 5, 15]
conds  = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]

'''
**********
IMPORTANT NOTE:
Condition Sep Pen
0         32  0
1         44  0 
2         32  1
3         44  1
4         32  3
5         44  3
6         32  5
7         44  5
8         32  15
9         44  15
'''

def main():
    
  
    for sub in all_subs:
        sub_dev_frame   = DataFrame()
        sub_est_frame   = DataFrame()
        sub_behav_frame = DataFrame()
        sub_behav_frame = pd.read_csv('standard_data/%s_standard_test_data.csv' % (sub))
        
        for mod in models:
            sub_dev_frame   = DataFrame()
            sub_est_frame   = DataFrame()
            sub_est_frame   = pd.read_csv('model_estimates/%s_%s_model_aim_estimates.csv' % (sub, mod))
            behav_col       = []
            est_col         = []
            cond_col        = []
            for cond in conds:
                x_behav = sub_behav_frame[sub_behav_frame['condition'] == cond].standardPokePosX
                y_behav = sub_behav_frame[sub_behav_frame['condition'] == cond].standardPokePosY
                x_behav = x_behav.tolist()
                y_behav = y_behav.tolist()
                x_est   = [sub_est_frame.iloc[0][2*cond]] * len(x_behav)
                y_est   = [sub_est_frame.iloc[0][2*cond + 1]] * len(y_behav)

                cond_est   = x_est + y_est
                cond_behav = x_behav + y_behav
                cond_cond  = [cond] * len(cond_behav)

                behav_col = behav_col + cond_behav
                est_col   = est_col + cond_est
                cond_col  = cond_col + cond_cond 

            std_col = [sqrt(sub_behav_frame['train1_var'].mean())] * len(behav_col)
            
            sub_dev_frame['poke'] = behav_col
            sub_dev_frame['est']  = est_col
            sub_dev_frame['cond'] = cond_col
            sub_dev_frame['std']  = std_col

            sub_dev_frame.to_csv('deviance_files/%s_%s_deviance_input.csv' % (sub, mod))


                
            



        

if __name__ == '__main__':
    main()
        
