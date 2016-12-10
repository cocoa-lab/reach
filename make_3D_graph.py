import scipy as sp
from scipy import stats
import pandas as pd
import numpy as np
import os
import errno
import matplotlib as mpl
from pandas import Series, DataFrame
from math import sqrt
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


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
models    = ['Y', 'N']

def main():
  for sub in all_subs:
    for mod in models:
      fig, ((ax1,ax6), (ax2, ax7), (ax3,ax8), (ax4, ax9), (ax5, ax10)) = plt.subplots(5,2, sharex='col', sharey='row')
      axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10]
      n = 0
      for sep in sep_dists:
        for pen in pen_vals:

          x_data, y_data = np.meshgrid(np.arange(-100, 100), np.arange(-100, 100))

          graph_data = pd.read_csv('/model_output/%s_%s_%s_%s_EV_graph_data.csv' % (sub, mod, sep, pen), index_col = None)
          ev_data    = graph_data['ev'].values

          if mod == 'Y':
            sub_data = pd.read_csv('/standard_data/%s_standard_test_data.csv' % (sub), index_col = None)
            la_score = sub_data['LossAversion'].mean()
          else:
            la_score = 1
          if pen in [3, 15]:
            rew = 3
          else:
            rew = 1

          ev_min = -pen*la_score
          ev_max = rew

          axes[n]  = fig.axes[n](projection='3d')

          surf = axes[n].plot_surface(x_data, y_data, ev_data, rstride=1, cstride=1, cmap=mpl.cm.Spectral, zorder = 1) #, alpha = 0.3
          cset = axes[n].contourf(x_data, y_data, z_data, offset = ev_min, cmap=mpl.cm.Spectral) 

          # filter out extra ticks that exceed data limits
          axes[n].set_zticks(filter(lambda x: z_min <= x <= z_max, ax.get_zticks()))
          axes[n].set_zlim(ev_min, ev_max)
          axes[n].set_xlim(-100, 100)
          axes[n].set_ylim(-100, 100)

          n+=1

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig(cwd + '/graphs/%s_%s_3D_EV_graph.pdf' %(sub, mod), bbox_inches = 'tight')
    plt.close()
    1/0      




# def create_EV_landscape(ev_array, condition, output_dir, optimal_input, sub, LA_score):

# [temp_horiz_min, temp_horiz_max] = get_horiz_min_max(condition)
# [temp_vert_min, temp_vert_max]   = get_vert_min_max(condition)

# if sub == 403:
#     temp_horiz_max = 40
#     temp_horiz_min = -70
#     temp_vert_max  = 55
#     temp_vert_min  = -55

# X = np.arange(temp_horiz_min, temp_horiz_max, SIM_GRID_GRAN)
# Y = np.arange(temp_vert_min, temp_vert_max, SIM_GRID_GRAN)

# # X = np.array(X)
# # Y = np.array(Y)

# X, Y = np.meshgrid(X, Y) #X.astype(np.int8), Y.astype(np.int8)

# temp_grid_width  = (abs(temp_horiz_min) + temp_horiz_max) * 1/SIM_GRID_GRAN
# temp_grid_height = temp_grid_width

# Z = np.zeros([temp_grid_width, temp_grid_height]) 

# #n = 0 

# #print np.shape(f)
# #print np.shape(ev_array)
# for i in ev_array:

#     x = i[0][0]
#     y = i[0][1]

#     x += abs(temp_horiz_min)
#     y += abs(temp_vert_min)

#     #print n

#     Z[y][x] = i[1]
#     #n += 1


# fig = plt.figure()
# ax  = fig.gca(projection='3d')


# cond  = get_condition_details(condition)

# z_min = cond[1]
# z_max = cond[2]

# if optimal_input in LOSS_AVERSION_MODELS:
#     z_min = cond[1] * abs(LA_score)

# surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=mpl.cm.Spectral, zorder = 1) #, alpha = 0.3

# if z_min == 0:
#     z_min = -0.5
# else:
#     z_min = z_min

# # temp_opt_point = opt_point_ev_pair[0]
# # opt_x = temp_opt_point[0]
# # opt_y = temp_opt_point[1]
# # opt_z = opt_point_ev_pair[1]

# #ax.scatter(opt_y, opt_x, opt_z, c = 'k', s = 75, marker = '*', zorder = 2)

# cset = ax.contourf(X, Y, Z, offset = z_min, cmap=mpl.cm.Spectral) #levels = levels
# # cset = ax.contourf(X, Y, Z, zdir='x', offset=temp_horiz_min, cmap=mpl.cm.Spectral)
# # cset = ax.contourf(X, Y, Z, zdir='y', offset=SIM_GRID_VERT_MAX, cmap=mpl.cm.Spectral)


# # filter out extra ticks that exceed data limits
# ax.set_zticks(filter(lambda x: z_min <= x <= z_max, ax.get_zticks()))
# ax.set_zlim(z_min, z_max)
# ax.set_zlabel('Z')
# ax.set_xlim(temp_horiz_min, temp_horiz_max)
# ax.set_xlabel('X')
# ax.set_ylim(temp_vert_min, temp_vert_max)
# ax.set_ylabel('Y')

# # ax.zaxis.set_major_locator(LinearLocator(10))
# # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# fig.colorbar(surf, shrink=0.5, aspect=5)

# plt.savefig(current_working_dir + output_dir + optimal_input + condition + '_'  + '_3D_EV_landscape.pdf', bbox_inches = 'tight')

# #plt.show()
plt.close()


if __name__ == '__main__':
    main()

