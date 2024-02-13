# Gama function

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt



def binned_plot(x,y, param_name, B):
    '''Shows standard plot of x vs. y
        Should have stellar mass as x variable
    '''
    #xy = np.vstack([x, y])
    #z = gaussian_kde(xy)(xy)

    # binning and statistics
    bin_medians, bin_edges, binnumber = stats.binned_statistic(x=x, values=y,statistic= 'median', bins = B)
    std, s_edges, s_binnumber = stats.binned_statistic(x=x, values = y, statistic = 'std', bins = B)

    plt.figure()

    plt.scatter(x, y, s = 1,color = 'slategray', alpha = 0.2)
    plt.title(f"{param_name} vs. Mass")
    plt.xlabel("Mass") ; plt.ylabel(f"{param_name}")

    # Errorbars 
    errbars = (bin_edges[1:] + bin_edges[:-1])/2        # x position of median points
    plt.errorbar(errbars ,bin_medians, yerr=std, fmt='k-')  # This plots median point x value, and median (which is y value)



def std_treatment(dataframe, parameter, num_sigmas):
    '''Treats outliers by removing how many standard deviations 
        away from mean/median you want to remove from data.
    '''
    std = np.std(dataframe[parameter])
    mean = np.mean(dataframe[parameter]) 
    median = np.median(dataframe[parameter]) 

    lower_bound = mean - (num_sigmas * std) 
    upper_bound = mean + (num_sigmas * std) 

    df = dataframe[ (dataframe[parameter] < upper_bound) & (dataframe[parameter] > lower_bound) ]
    
    return df


def resmask(delta_param):
    '''Similar to std_treatment. However, takes in individual
     arrays and creates mask for other two parameters.
     We only want most significant outliers to be removed, 
     so sigma is set to 4 in the function. (maybe make this optional argument later)
     '''
    lowerbound = np.mean(delta_param) - (4 * np.std(delta_param))
    upperbound = np.mean(delta_param) + (4 * np.std(delta_param))

    mask = (delta_param < upperbound) & (delta_param > lowerbound)

    return mask



def iqr_treatment(datacolumn):
    '''Treats outliers by using IQR method'''
    sorted(datacolumn)
    Q1,Q3 = np.percentile(datacolumn , [16,84])
    IQR = Q3 - Q1
    lower_range = Q1 - (2 * IQR)
    upper_range = Q3 + (2 * IQR)
    
    return lower_range,upper_range



def mass_decoupler(x, y, B): 
    '''Takes a parameter in and decouples mass from it, 
        returning the Delta Parameter.
        Stellar mass should be x variable.'''

        # Statistics calculations 
    #B = 12
    bin_medians, bin_edges, binnumber = stats.binned_statistic(x=x, values=y,statistic= 'median', bins = B)
    std, s_edges, s_binnumber = stats.binned_statistic(x=x, values = y, statistic = 'std', bins = B)
    errbars = (bin_edges[1:] + bin_edges[:-1])/2 

        # Slope calculations 
    x1 = errbars[:-1] ; x2 = errbars[1:]
    y1 = bin_medians[:-1] ; y2 = bin_medians[1:]
    m = (y2 - y1) / (x2 - x1) # slope
    b = -m*x1 + y1            # y-intercept

        # Delta Parameter Calculation 
    y_exp = np.zeros(len(y))  # y_expected array
    i = 0
    while i < len((x)):
        xi = x[i]
        for n in range(B-1): # had to be 1 less than 3 of bins
            if xi <= errbars[n] and xi >= errbars[n-1]:
                Y = m[n] * xi + b[n]
                y_exp[i] = Y 
                deltaParam = y - y_exp
            else:
                pass
        i+=1
    
    residuals = y - y_exp

    return deltaParam, y_exp, residuals 



def mass_decoupler_masked(x, y, B): 
    '''Takes a parameter in and decouples mass from it, returning the Delta Parameter.
        Stellar mass should be x variable. Treats delta parameter outliers using 
        standard dev. of 4 and higher and masking.
        x and y must be numpy arrays.
        '''
    deltaParam, y_exp, residuals = mass_decoupler(x, y, B)

    dmask = resmask(deltaParam)

    delta_param = deltaParam[dmask]
    yexp = y_exp[dmask]
    res = residuals[dmask]
    X = x[dmask] # the original "X" array (which has typically been logmstar); sliced by dmask 
 
    return delta_param, y_exp, res, X, dmask 
