#metric_functions.py

import numpy as np
import time as time

#function created by Janvi Madhani for use in plotting filaments using dictionary she created
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


#function to slice a dictionary list by a particular set of keys 
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


#function to get the coordinates (if px,py, and pz are separate) for each CP type
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


#simple distance calculation function
def distance(filament):
    '''Calculates the total distance between all points of a given (half) filament.
        Returns one value which is the total distance from one CP of filament to other CP.'''
    N = len(filament)
    for i in range(N): 
        a = filament[1:] ; b = filament[:-1] #makes two even array from original array - to subtract nicely 
        x1 = a[:,0] ; y1 = a[:,1] ; z1 = a[:,2]
        x2 = b[:,0] ; y2 = b[:,1] ; z2 = b[:,2]
        distances = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        dist = np.sum(distances) ; return dist
    

#function to get coordinates from filament dictionary
def Fil_Coordinates(fils):
        ''''Takes filament dictionary/list and returns an 
            array of all px, py, pz values.'''
        N = len(fils) ; coords_list = [] 
        for i in range(N): 
            c = fils[i]['px,py,pz']
            coords_list.append(c)
        #vectorizes list of coordinates
        N = len(coords_list) ; coordinates = []
        for i in range(N): 
            array = np.array(coords_list[i])
            coordinates.append(array)
        return coordinates


#function to calculate half distances
def Fil_Half_Distances(fils): 
    '''Takes filament dictionary/list and returns
        the half distances of the filaments.'''
    coordinates = Fil_Coordinates(fils) #uses previosuly defined function to get coordinates
    N = len(coordinates) ; FHL = np.zeros(N) #this is the part that calculates half distances
    for i in range(N): 
        filament = coordinates[i]
        d = distance(filament)
        FHL[i] = d
    return FHL








#CLASSES??? 
# This class works! However how to get subsequent functions to "talk" to each other?
class Filament_Half_Distances():
    '''Takes array of filament data and calculates the half distance'''
    def __init__(self, fils): #init method or constructor
        self.fils = fils

    def coordinates(self): #method 1 (after the __init__ constructor)
        ''''Takes filament dictionary/list and returns array 
            of all px, py, pz values'''
        N = len(self.fils) ; coords_list = [] 
        for i in range(N): 
            c = self.fils[i]['px,py,pz']
            coords_list.append(c)
        
        N = len(coords_list) ; coordinates = []
        for i in range(N): 
            array = np.array(coords_list[i])
            coordinates.append(array)
        return coordinates
#a call for this class in a notebook looks as follows: 
# import filament_metrics as fm 
# fils = filament_dm_dict['filaments'] 
# F = fm.Filament_Half_Distance(fils)
# F.coordinates() 
##this is what returns the coordinates (and works!) but adding more functions in class does not work 

