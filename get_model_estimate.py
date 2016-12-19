import pandas as pd
import os
from pandas import Series, DataFrame
from math import sqrt
all_subs = []

for n in range(403, 550):
    try: 
        temp_frame = pd.read_csv('model_output/%s_N_32_15_EV_graph_data.csv' % (n), index_col = 0)
        if n != 999:
            all_subs.append(n)
    except: 
        continue        

models = ['N', 'Y']
seps   = [32, 44]
pens   = [0, 1, 3, 5, 15]
conds  = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]

def main():
    print all_subs
    1/0
    
    for sub in all_subs:
        for mod in models:
            sub_frame = DataFrame()
            for sep in seps:
                for pen in pens:
                    temp_frame = pd.read_table('model_output/%s_%s_%s_%s_EV_graph_data.csv' % (sub, mod, sep, pen), sep = None)
               
                    max_idx = temp_frame['ev'].idxmax()
                    max_ev  = temp_frame['ev'].max()
                    mEV_frame = temp_frame[temp_frame['ev'] == max_ev]
                    
                    if len(mEV_frame) > 1:
                        mEV_frame = mEV_frame.reset_index(drop=True)
                        opt_y  = [mEV_frame['y_aim'].mean()]
                        opt_x  = [mEV_frame['x_aim'].mean()]
                    else: 
                        opt_y   = [temp_frame.iloc[max_idx]['y_aim']]
                        opt_x   = [(temp_frame.iloc[max_idx]['x_aim'])]
                        
                    sub_frame['X_%s_%s' % (sep, pen)] = opt_x
                    sub_frame['Y_%s_%s' % (sep, pen)] = opt_y
            
            sub_frame.to_csv('model_estimates/%s_%s_model_aim_estimates.csv' % (sub, mod), index=False)        




if __name__ == '__main__':
    main()
        