import os
import pandas as pd
from pandas import Series, DataFrame
from math import sqrt

all_subs = []

for n in range(403, 550):
	try: 
		temp_frame = pd.read_csv('model_estimates/%s_Y_model_aim_estimates.csv' % (n), index_col = 0)
		if not(n in [407, 410, 500]):
			all_subs.append(n)
	except: 
		continue        

seps   = [32, 44]
pens   = [0, 1, 3, 5, 15]
NUM_CONDITIONS = 10

print all_subs

def main():

	df = DataFrame()
	ltv_x  = []
	nltv_x = []
	ltv_y  = []
	nltv_y = []
	lcv_x  = []
	nlcv_x = []
	lcv_y  = []
	nlcv_y = []
	avg_x    = []
	avg_y    = []
	la_score = []
	cond_var = []
	tot_var  = []
	subs     = []
	sep_dist = []
	pen_val  = []

	for sub in all_subs:
		nltv_estimates = pd.read_csv('model_estimates/%s_nltv_model_aim_estimates.csv' %(sub))
		ltv_estimates  = pd.read_csv('model_estimates/%s_ltv_model_aim_estimates.csv' %(sub))  
		nlcv_estimates = pd.read_csv('model_estimates/%s_nlcv_model_aim_estimates.csv' %(sub))
		lcv_estimates  = pd.read_csv('model_estimates/%s_lcv_model_aim_estimates.csv' %(sub))      	
		behav        = pd.read_csv('standard_data/%s_standard_test_data.csv' %(sub))
		var_frame    = pd.read_csv('standard_data/%s_condition_variances.csv' %(sub))	
		for sep in seps:
			sep_behav  = behav[behav['absoluteSepDist'] == sep]
			for pen in pens:           	
				cond_behav = sep_behav[sep_behav['penaltyVal'] == -pen]
				avg_x.append(cond_behav.standardPokePosX.mean())
				avg_y.append(cond_behav.standardPokePosY.mean())
				cond_var.append(var_frame.get_value(0,'%s,%s' %(sep, pen)))
				ltv_x.append(ltv_estimates.get_value(0,'X_%s_%s' %(sep, pen)))
				ltv_y.append(ltv_estimates.get_value(0,'Y_%s_%s' %(sep, pen)))
				nltv_x.append(nltv_estimates.get_value(0,'X_%s_%s' %(sep, pen)))
				nltv_y.append(nltv_estimates.get_value(0,'Y_%s_%s' %(sep, pen)))
				lcv_x.append(lcv_estimates.get_value(0,'X_%s_%s' %(sep, pen)))
				lcv_y.append(lcv_estimates.get_value(0,'Y_%s_%s' %(sep, pen)))
				nlcv_x.append(nlcv_estimates.get_value(0,'X_%s_%s' %(sep, pen)))
				nlcv_y.append(nlcv_estimates.get_value(0,'Y_%s_%s' %(sep, pen)))

				sep_dist.append(sep)
				pen_val.append(pen)

		tot_var +=[behav.get_value(0,'train1_var')]*NUM_CONDITIONS  
		la_score+=[-behav.get_value(0, 'LossAversion')]*NUM_CONDITIONS 
		subs    +=[sub]*NUM_CONDITIONS
	
	dd = {'ltv_x': ltv_x, 'ltv_y': ltv_y, 'nltv_x': nltv_x, 'nltv_y': nltv_y, 
	      'lcv_x': lcv_x, 'lcv_y': lcv_y, 'nlcv_x': nlcv_x, 'nltv_y': nlcv_y,
	       'avg_x': avg_x, 'avg_y': avg_y, 'abs_lambda': la_score, 'cond_var': cond_var,
	       'tot_var': tot_var, 'sub': subs, 'sep_dist': sep_dist, 'pen_val': pen_val}
	df = DataFrame(data=dd)
	df.to_csv('model_estimates/all_behav_model_data.csv')




if __name__ == '__main__':
	main()