#kd_tree.py

import numpy as np
from scipy import spatial 
#KD Tree implemenation - quite short and doesn't really have to be its own function but just to have here: 
def kdtree_twoarrays(array1, array2, N_nearest_neighbors):
    '''Simple KDTree that checks all the points in one array against all the 
    points in the other and returns 1) the distance and 2) the indeces. 
    (Each element/point of the array will correspond to 'N_neareset_neighbors') 
    # of indeces.'''
    distance, index = spatial.KDTree(array1).query(array2, k = N_nearest_neighbors) #array2 would be galaxies and array1 filament points
    return distance, index 