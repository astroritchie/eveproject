'''
Open txt file
Sum and peak flux for each line
'''

import numpy as np
import os

def calcSumPeak():
    
    np.set_printoptions(precision = 27)
    
    directory = '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/FlareTxtFiles/'
    
    allSums = np.zeros((3139,39),dtype=np.float64)
    allPeaks = np.zeros((3139,39),dtype=np.float64)
    
    # (0,i) is total number of data points
    # (1,i) is total number of missing data points
    
    flare = 0    
    
    nobackground = 0
    
    for filename in sorted(os.listdir(directory)):    
        if filename.endswith('.txt'):
    
            data = np.loadtxt(directory+filename,delimiter=',',dtype=float)
            
            for i in range(0,39):                                
                lineflux = data[1:,i+1] # 0th column (:,0) is time in SOD of measurement in that row           
                
                missing = 0
                
                datalength = np.count_nonzero(lineflux)
                
                background = lineflux[0]
                
                for j in range(len(lineflux)):
                    
                    if background < 0:
                        lineflux[j] = 0
                        nobackground += ( 1 / len(lineflux))
                    
                    elif lineflux[j] < 0:
                        missing +=1
                        lineflux[j] = 0
                    
                    else:
                        lineflux[j] = lineflux[j] - background
                        
                allSums[0,i] = allSums[0,i] + datalength
                allSums[1,i] = allSums[1,i] + missing
                allSums[flare+2,i] = sum(lineflux)
                
                allPeaks[0,i] = allPeaks[0,i] + datalength
                allPeaks[1,i] = allPeaks[1,i] + missing
                allPeaks[flare+2,i] = max(lineflux)
                
            flare+=1
            print(flare)
    
    print('Number of flare events with background errors:',nobackground)
    
    for i in range(39):
        print(float(allSums[1,i] / allSums[0,i]) * 100,'% missing sum values for line',i)
        print(float(allPeaks[1,i] / allPeaks[0,i]) * 100,'% missing peak values for line',i)
            
    np.savetxt(directory+'/total/bgsFlareSums.txt', allSums,fmt = '%1.10f',delimiter=';')
    np.savetxt(directory+'/total/bgsFlarePeaks.txt', allPeaks,fmt = '%1.10f',delimiter=';')
        
calcSumPeak()