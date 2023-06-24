# myfunctions.py 

import numpy as np

#function created by Janvi Madhani
def plot_dm_filament(filament_idx,filament_dict,ax,colorfil='slateblue'):
    '''Helps plot filaments'''
    nsamp = filament_dict['filaments'][filament_idx]['nsamp'] 
    positions = filament_dict['filaments'][filament_idx]['px,py,pz']
    #plot the samples in between
    px = []
    py = []
    pz = []   
    for i in range(nsamp):
        px_,py_,pz_ = positions[i][0],positions[i][1],positions[i][2]
        px.append(px_)
        py.append(py_)
        pz.append(pz_)

    
    fil_line = ax.plot3D(px,py,pz,c=colorfil,lw = '2',alpha=0.4)



#define function to slice a dictionary list by a particular set of keys 
def dict_slice(dict, key, value):
    '''Indexes/slices a subset of a larger dictionary. 
        For use with separating critical points (since the CP id's are gven).
        Output is a list of dictionaries.'''
    N = len(dict)

    list = []
    for i in range(N):
        C = dict[i][key]
        if C == value:
            list.append(dict[i])
    return list 



#define a function to get the coordinates (if px,py, and pz are separate) for each type
def cp_plotter(cp):
    '''If the coordinates for a CP are separated by x,y,z 
        then this returns an array with all the values for 
        that critical point.(Perhaps too specialized - come back 
        and generalize for other use besides coordinates)'''
    N = len(cp)
    coordinates = np.zeros((N,3))
    x = 3
    
    for i in range(N): 
        coordinates[i,0] = cp[i]['px']
        coordinates[i,1] = cp[i]['py']
        coordinates[i,2] = cp[i]['pz']
    x = coordinates[:,0] ; y = coordinates[:,1] ; z = coordinates[:,2]
    return x, y, z