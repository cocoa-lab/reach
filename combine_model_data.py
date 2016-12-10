import pandas as pd 
import os 
from pandas import Series, DataFrame
from math import sqrt

all_subs = []

for n in range(403, 550):
    try: 
        temp_frame = pd.read_csv('model_output/%s_N_model_aim_estimates.csv' % (n), index_col = 0)
        if n != 999:
            all_subs.append(n)
    except: 
        continue

models    = ['N', 'Y']

def main():
    

    for mod in models:

        all_mod_frame = DataFrame()
        all_ev_frame  = DataFrame()

        for sub in all_subs:

            temp_mod_frame = pd.read_csv('model_output/%s_%s_model_aim_estimates.csv' % (sub, mod), index_col = 0)
            temp_ev_frame  = pd.read_csv('model_output/%s_%s_model_EV_estimates.csv' % (sub, mod), index_col = 0)

            temp_mod_frame['sub'] = sub
            temp_ev_frame['sub']  = sub
            
            all_mod_frame  = pd.concat([all_mod_frame, temp_mod_frame])
            all_ev_frame   = pd.concat([all_ev_frame, temp_ev_frame])


        all_mod_frame.to_csv('all_%s_model_aim_estimates.csv' % (mod))
        all_ev_frame.to_csv('all_%s_model_EV_estimates.csv' % (mod)) 


if __name__ == '__main__':
    main()
