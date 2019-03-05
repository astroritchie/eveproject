'''
Sum and peak flux for each line
'''

import numpy as np
import os

def calcSumPeak():
    
    directory = '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/FlareTxtFiles/'
    
    allSums = np.empty((3137,39),dtype=float)
    allPeaks = np.empty((3137,39),dtype=float)
    
    flare = 0

    sums = np.empty((39),dtype=float)
    peaks = np.empty((39),dtype=float)
    
    for filename in os.listdir(directory):
        if filename.endswith('.gz'):
    
            data = np.loadtxt(directory+filename,delimiter=',')
            for i in range(0,39):
                allSums[flare,i] = sum(data[:,i])
                allPeaks[flare,i] = max(data[:,i])
                
            flare+=1
            print(flare)

    np.savetxt(directory+'/total/FlareSums.txt.gz', allSums,fmt = '%f',delimiter=';')
    np.savetxt(directory+'/total/FlarePeaks.txt.gz', allPeaks,fmt = '%f',delimiter=';')
        
calcSumPeak()