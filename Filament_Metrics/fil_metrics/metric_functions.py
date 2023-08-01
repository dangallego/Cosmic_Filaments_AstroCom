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


#function to find saddle critical points with desired number of nfils attached
def cp_nfils(critical_points, CP_ID, nfils):
    '''Takes dicitonary of critical points and input of desired nfils.
        Returns dicitonary of desired critical_point ID type with 
        the desired number of filaments attached. 
        Mainly for use with saddles to get saddles with nfils  == 2.'''
    cp_type = dict_slice(critical_points, 'cp_idx', CP_ID)
    cp_nfils = [] ; N = len(cp_type) 

    for i in range(N): 
        nfils = nfils
        if cp_type[i]['nfil'] == nfils: 
            cp_nfils.append(cp_type[i])
    return(cp_nfils)


#function that gives the filaments with cp indices corresponding to nfil == 2
def filaments_nfil2(filament_dict, critical_points):
    '''Builds on cp_nfils array by taking the result of finding 
        saddles with nfil == 2 and using the \'filID\'s\' of each
         of those saddles to slice the original filament dictionary.
         Result is a reduced dictionary of what should be proper half filaments 
         (each filament in the dictionary corresponds to saddles with nfils == 2).'''
    saddles_nfils = cp_nfils(critical_points, 2, 2) #creates selective saddle dictionary with nfil == 2
    #finds index of half filaments 
    filIDs = np.zeros(len(saddles_nfils)) ; filIDs2 = np.zeros(len(saddles_nfils))
    for i, filID in enumerate(saddles_nfils):
        filIDs[i] = saddles_nfils[i]['destID,filID'][0][1]
        filIDs2[i] = saddles_nfils[i]['destID,filID'][1][1]
    fil_ids = np.append(filIDs, filIDs2) ; fil_ids = np.sort(fil_ids) ; fil_ids = (np.rint(fil_ids)).astype(int)
    fils_nfils2 = [filament_dict[i] for i in fil_ids]
    return fils_nfils2


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
        ''''Takes filament dictionary/list and returns a
            list of all px, py, pz values.'''
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

#alternative to Fil_Coordinates that returns a 1d array of all filament coordinates
def Fil_Coordinates1D(fils):
    '''Takes filament dictionary/list and returns a 
    1D array of all px,py,pz values.'''
    coordinates = [] ; N = len(fils)
    for i in range(N): 
        c = fils[i]['px,py,pz']
        coordinates.append(c)
    flat_coordinates = [num for sublist in coordinates for num in sublist]
    pointcloud = np.array(flat_coordinates)
    return pointcloud 



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

#function to find the shortest galaxy - filament distances, while accounting for the line between filament segment extremities
def galfildist(galaxies, filament_points, KDTindex):
    '''Finds closest distance between an array of galaxies and 
        an array of filament points. The filament_points array must be 
        segmented so that the first element corresponds to the first pair of points
        (which correspond to the first two points of a filament segment's extremity).
        This code is optimized and intended to be used AFTER implementing a KDTree.
        KDTindex must correspond to the index array that comes out of using KDTree.'''
    shortest_distances = np.zeros(len(galaxies))
    for h in range(len(galaxies)):
        distances = np.zeros(len(KDTindex[0]))
        workingarray = filament_points[KDTindex[h]]
        for i in range(len(workingarray)):
            A = workingarray[i,:-4] ; B = workingarray[i,3:-1] ; AB = B - A ; AG = galaxies[h] - A
            u = AB / np.linalg.norm(AB)
            #Loop over here
            if np.dot(AG, u) < 0:
                distances[i] = np.linalg.norm(galaxies[h] - A)
            elif np.dot(AG, u) > np.linalg.norm(AB):
                distances[i] = np.linalg.norm(galaxies[h] - B)
            elif np.dot(AG, u) < np.linalg.norm(AB):
                distances[i] = np.linalg.norm((np.cross((A-B), (A-galaxies[h])))) / (np.linalg.norm(galaxies[h]-B))
        shortest_distances[h] = np.min(distances)
    return shortest_distances


