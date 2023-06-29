#Read_Fils_Plotter.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits import mplot3d
from matplotlib import cm
import mpl_toolkits.mplot3d.art3d as art3d
import os
import pandas as pd
matplotlib.rcParams['font.family'] = [ 'serif']
matplotlib.rcParams['agg.path.chunksize'] = 10000

import sys  #points to Janvi's directory and functions
sys.path.insert(0, '/Users/Daniel/Documents/Research Projects/Cosmic Filaments/example_filaments')
import read_fils as rf #imports functions created by Janvi Madhani for use in plotting filaments from dict

sys.path.insert(0, '/Users/Daniel/Documents/Research Projects/Cosmic Filaments/Filament_Metrics' )
import fil_metrics.metric_functions as fm #imports functions created by Daniel in filament metrics and properties

skeleton_file_dm = '/Users/Daniel/Documents/Research Projects/Cosmic Filaments/example_filaments/del_galaxy.NDnet_s5.up.NDskl.BRK.a.NDskl'
filaments_dm = rf.ReadFilament(skeleton_file_dm)
filament_dm_dict = filaments_dm.filament_dict
print(filament_dm_dict)

#separate 'filaments' and 'critical_points' dictionaries (each is now a list of dictionaries)
fils = filament_dm_dict['filaments'] ; crit_points = filament_dm_dict['critical_points'] 

#number of filaments
nfils = filament_dm_dict['nfils'] ; ncrit = filament_dm_dict['ncrit']

voids = fm.dict_slice(crit_points, 'cp_idx',0)
walls = fm.dict_slice(crit_points, 'cp_idx',1)
saddles = fm.dict_slice(crit_points, 'cp_idx',2)   #filament saddles
peaks = fm.dict_slice(crit_points, 'cp_idx',3)     #peaks -- nodes! 
bi_points = fm.dict_slice(crit_points, 'cp_idx',4) #bifurcation points

##TRYING to make sense of saddles
real_saddles = [] # try with "real" saddles (no boundary)
N = len(saddles)
for i in range(N):
    if saddles[i]['boundary'] == 0.0:
        real_saddles.append(saddles[i])

saddles_nfils = [] ; N = len(saddles) #list of saddles with 'nfils' == 2 (as saddles should be)
for i in range(N): 
    n_fils = 2 #decide here how many nfils we want to check in saddles
    if saddles[i]['nfil'] == n_fils: 
        saddles_nfils.append(saddles[i])
len(saddles_nfils)


#Make scatter plot 
fig = plt.figure(figsize=[8,8]) ; ax = fig.add_subplot(projection='3d')
ax.set_box_aspect([1,1,1])

for fil_idx in range(nfils): #plots the filaments 
    fm.plot_dm_filament(fil_idx,filament_dm_dict,ax)


#plots the critical points
x,y,z = fm.cp_plotter(voids) ; ax.scatter(x,y,z, label = 'Voids', c = 'k', s = 200, alpha = 0.1)
x,y,z = fm.cp_plotter(walls) ; ax.scatter(x,y,z, label = 'Walls', s = 25, alpha = 0.5, c = 'gold')
x,y,z = fm.cp_plotter(peaks) ; ax.scatter(x,y,z, label = 'Nodes', s = 100, alpha = 0.5, c = 'tomato')
x,y,z = fm.cp_plotter(bi_points) ; ax.scatter(x,y,z, label = 'Bi. Points', s = 10, alpha = 0.5, c = 'k')

#saddles
#x,y,z = myfunctions.cp_plotter(saddles) ; ax.scatter(x,y,z, label = 'Saddles', s = 40, alpha = 0.4, c = 'darkturquoise')
#x,y,z = myfunctions.cp_plotter(real_saddles) ; ax.scatter(x,y,z, label = 'Saddles (no boundary)', s = 40, alpha = 0.4, c = 'darkturquoise')
x,y,z = fm.cp_plotter(saddles_nfils) ; ax.scatter(x,y,z, label = 'Saddles w/ nfils=2', s = 40, alpha = 0.4, c = 'darkturquoise')

ax.set_xlabel('X') ; ax.set_ylabel('Y') ; ax.set_zlabel('Z')
ax.legend()
extent = 10
ax.set_xlim(-extent,extent)
ax.set_ylim(-extent,extent)
ax.set_zlim(-extent,extent)
plt.show()
