'''
Open txt file
Sum and peak flux for each line
'''

import numpy as np
import os

def calcSumPeak():
    
    np.set_printoptions(precision = 27)
    
    directory = '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/FlareTxtFiles/'
    
    allSums = np.empty((3137,39),dtype=float)
    allPeaks = np.empty((3137,39),dtype=float)
    
    flare = 0
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
    
            data = np.loadtxt(directory+filename,delimiter=',',dtype=float)
            
            for i in range(0,39):
                #allSums[flare,i] = sum(data[flare,i])
                #allPeaks[flare,i] = max(data[flare,i])
                #allPeaks[flare,i] = data.max(axis=0)[i+1]
                #allSums[flare,i] = data.sum(axis=0)[i+1]
                allPeaks[flare,i] = np.amax(data,axis=0)[i+1]
                allSums[flare,i] = np.sum(data,axis=0)[i+1]
            
                
            flare+=1
            print(flare)
            
    np.savetxt(directory+'/total/FlareSums.txt', allSums,fmt = '%1.10f',delimiter=';')
    np.savetxt(directory+'/total/FlarePeaks.txt', allPeaks,fmt = '%1.10f',delimiter=';')
        
calcSumPeak()