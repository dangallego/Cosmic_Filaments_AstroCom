#matplotlib 
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
import sys  
sys.path.insert(0, '/Users/zaraafrooz/Desktop/Cosmic_Filaments_AstroCom/filament_work_zara/example_filaments')
import read_fils as rf
skeleton_file_dm = '/Users/zaraafrooz/Desktop/Cosmic_Filaments_AstroCom/filament_work_zara/example_filaments/del_galaxy.NDnet_s5.up.NDskl.BRK.a.NDskl'
filaments_dm = rf.ReadFilament(skeleton_file_dm)
filament_dm_dict = filaments_dm.filament_dict

def filkey(key):
    if key == 'keys':
        print(filament_dm_dict.keys())
    else:
        print(filament_dm_dict.keys())
        for items in filament_dm_dict:
            print("these are the " + key + " in the Filament Dictionary")
            print(filament_dm_dict[key])
            if type(filament_dm_dict[key]) == 'int':
                print("the numbers of items in this list is " + str(len(filament_dm_dict[key])))
            break


print("All necessary libraries imported")

#filkey()

#to look at what's in the dictionary and what number from the field value something correlates to, call filkey().
fil = filament_dm_dict['filaments']
crtp= filament_dm_dict['critical_points']
fivals= 'Field Vals'

#testing to see if the above shortcuts work.
#print(fil[0])

#critical point field values
def cvals(i,j,k):
    pr = []
    for cp in crtp:
        if j>4 or i>4:
                print("Both i and j must be between 0-4")
                break
        elif j == i: #to only want field values for cp_idx == i, set i == j 
            if cp['cp_idx'] == i:
                p = cp[fivals][k]
                pr.append(p)
        elif j>i: #to want to look at field values for cp_idx i to j, for example to see all the values from voids to peaks use i = 0 and j = 3
            if cp['cp_idx'] >= i:
                p = cp[fivals][k]
                pr.append(p)
        else:
            print("i must be less than j")
            break
    print("There are " + str(len(pr)) + " items in this call")
    return pr

#to call for any CP Field for any given index values or between two index values, use function cvals(i,j) where i and j are the index values of interest.

#plt.hist(cvals(0,4,1))
#plt.show()

#def fvals(i,j,k):

#filkey('critical_points')

filkey('CP_fields')

print(cvals(0,4,2))

