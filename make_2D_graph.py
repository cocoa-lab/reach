import pandas as pd
import pandas as pd
import os
import errno
import matplotlib as mpl
from pandas import Series, DataFrame
from math import sqrt
from matplotlib import pyplot as plt

cwd = os.getcwd()

all_subs = []
for n in range(403, 550):
    try: 

        temp_frame = pd.read_csv('model_estimates/%s_Y_model_aim_estimates.csv' %(n))
        if n != 999:
            all_subs.append(n)
    except: 
        continue

sep_dists = [32, 44]
pen_vals  = [0, 1, 3, 5, 15]

def main(): 
    for sub in all_subs:
        sub_graphs = []
        n = 0
        fig, ((ax1,ax6), (ax2, ax7), (ax3,ax8), (ax4, ax9), (ax5, ax10)) = plt.subplots(5,2, sharex='col', sharey='row')
        axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10]
        for sep in sep_dists:
            for pen in pen_vals:

                behavior_data     = pd.read_csv('standard_data/%s_standard_test_data.csv' %(sub))
                loss_estimates    = pd.read_csv('model_estimates/%s_Y_model_aim_estimates.csv' %(sub))
                no_loss_estimates = pd.read_csv('model_estimates/%s_N_model_aim_estimates.csv' %(sub))

                sep_behav_frame   = behavior_data[behavior_data['absoluteSepDist'] == sep]
                cond_behav_frame  = sep_behav_frame[sep_behav_frame['penaltyVal'] == -pen]
                
                all_behav_x   = cond_behav_frame['standardPokePosX'].values
                all_behav_y   = cond_behav_frame['standardPokePosY'].values
                avg_behav_x   = cond_behav_frame['standardPokePosX'].mean()
                avg_behav_y   = cond_behav_frame['standardPokePosY'].mean()
                loss_est_x    = loss_estimates['X_%s_%s' %(sep, pen)].mean()
                loss_est_y    = loss_estimates['Y_%s_%s' %(sep, pen)].mean()
                no_loss_est_x = no_loss_estimates['X_%s_%s' %(sep, pen)].mean()
                no_loss_est_y = no_loss_estimates['Y_%s_%s' %(sep, pen)].mean()

                axes[n].plot(all_behav_x, all_behav_y, "o", ms = 1.5, color='black', zorder = 1)
                

                avg_behav   = plt.Circle((avg_behav_x, avg_behav_y), 1.5 ,color='m',fill=True)
                loss_est    = plt.Circle((loss_est_x, loss_est_y), 1.5 ,color='y',fill=True)
                no_loss_est = plt.Circle((no_loss_est_x, no_loss_est_y), 1.5 ,color='c',fill=True)
                target      = plt.Circle((0,0),  32, color='g',fill=False)
                penalty     = plt.Circle((-sep,0), 32, color='r', fill=False) 
                
                axes[n].add_artist(target)
                axes[n].add_artist(penalty)
                axes[n].add_artist(avg_behav)
                axes[n].add_artist(loss_est)
                axes[n].add_artist(no_loss_est)
                axes[n].set_title('%s_%s' %(sep, pen))
                axes[n].set_xlim([-100, 100])
                axes[n].set_ylim([-50, 50])

                fig.legend((avg_behav, loss_est, no_loss_est), ('Average', 'Loss', 'Non-loss'), 'upper center')
            

                n += 1

        fig.set_size_inches((9, 12))

        path = cwd  + '/graphs/%s/' % (sub)
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        plt.savefig(cwd + '/graphs/%s/%s_2D_behav_avg_est.pdf' %(sub, sub))
        plt.close(fig)
        


if __name__ == '__main__':
    main()























        