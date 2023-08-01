# classes.py

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