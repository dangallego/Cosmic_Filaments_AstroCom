#importing operating system, path, and read_fils from Janvi's files
import os
import sys  
sys.path.insert(0,'/Users/zaraafrooz/Desktop/Cosmic_Filaments_AstroCom/filament_work_zara/example_filaments')
import read_fils as rf
skeleton_file_dm = '/Users/zaraafrooz/Desktop/Cosmic_Filaments_AstroCom/filament_work_zara/example_filaments/del_galaxy.NDnet_s5.up.NDskl.BRK.a.NDskl'
filaments_dm = rf.ReadFilament(skeleton_file_dm)
filament_dm_dict = filaments_dm.filament_dict


#allowing users to input GAMA file path based on the sigma of interest
input_filepath = input('Enter GAMA file path: ')
if os.path.exists(input_filepath):
    skeleton_GAMA = input_filepath
    filaments_GAMA = rf.ReadFilament(skeleton_GAMA)
    GAMA_dict = filaments_GAMA.filament_dict


#function below can be used to call keys from the GAMA data
def gamkey(key):
    if key == 'keys':
        print(GAMA_dict.keys())
    else:
        print(GAMA_dict.keys())
        for items in GAMA_dict:
            print("these are the " + key + " in the Filament Dictionary")
            print(GAMA_dict[key])
            if type(GAMA_dict[key]) == 'int':
                print("the numbers of items in this list is " + str(len(filament_dm_dict[key])))
            break

#function below can be used to call the data from Janvi's filament data
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

#setting necessary variables for the upcoming functions
fil = filament_dm_dict['filaments']
crtp= filament_dm_dict['critical_points']
fivals= 'Field Vals'

GAMfil = GAMA_dict['filaments']
GAMcp = GAMA_dict['critical_points']
GAMvals = 'Field Vals'

#critical point field values
#to call for any CP Field for any given index values or between two index values, use function cval(i,j,k) or gamc(i,j,k) where i and j are the index of interest
def cval(i,j,k):
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

def gamc(i,j,k):
    gpr = []
    for cp in GAMcp:
        if j>4 or i>4:
                print("Both i and j must be between 0-4")
                break
        elif j == i: #to only want field values for cp_idx == i, set i == j 
            if cp['cp_idx'] == i:
                p = cp[GAMvals][k]
                gpr.append(p)
        elif j>i: #to want to look at field values for cp_idx i to j, for example to see all the values from voids to peaks use i = 0 and j = 3
            if cp['cp_idx'] >= i:
                p = cp[GAMvals][k]
                gpr.append(p)
        else:
            print("i must be less than j")
            break
    print("There are " + str(len(gpr)) + " items in this call")
    return gpr

#filament field values
#to call for any filament Field for any given index values or between two index values, use function fval(i,j,k) or gamf(i,j,k) where i and j are the index of interest
def fval(k):
    f = []
    if k > (len(filament_dm_dict['fil_fields'])-1):
        print("There are only " + str(len(filament_dm_dict['fil_fields'])) + " Field Val inputs")
    else:
        for fils in fil:
            p = fils[fivals][k]
            f.append(p)
        print("There are " + str(len(f)) + " items in this call")
        return f

def gamf(k):
    g = []
    if k > (len(GAMA_dict['fil_fields'])-1):
        print("There are only " + str(len(GAMA_dict['fil_fields'])) + " Field Val inputs")
    else:
        for fils in GAMfil:
            p = fils[GAMvals][k]
            g.append(p)
        print("There are " + str(len(g)) + " items in this call")
        return g