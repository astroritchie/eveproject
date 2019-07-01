'''
Author:
Kent Ritchie

Purpose:
Calculate total flux and peak flux values for each flare event in RibbonDB for AIA emission lines
Same function as calcSumPeak but for AIA lines only

Function:
calcAIASumPeak()

Parameters:
save: if True will save .txt files as formatted below in Saves description

Needs:
3137 .txt files corresponding to flux information for each flare event in RibbonDB as created by createTxtFiles()
numpy, os libraries

Subfunction Invocations:
None

Returns:
fluxSums, fluxPeaks arrays

Saves:
2 separate .txt files, 1 containing total flux values and 1 containing peak flux values
Both .txt files contain the total number of data points and total number of missing data points

Both .txt files have shape (3139,39) where:
Rows correspond to the 39 EVE emission lines
0th column contains number of data points for respective line
1st column contains number of missing data points for respective line
2nd-3139th columns contain either total flux or peak flux values for each event per respective line

Updates:
6-29-19: Created as separate function from calcSumPeak
'''

import numpy as np
import os
import openRibbonDB

def calcAIASumPeak(save):

    directory = '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/AIALinesFluxTxtFiles/'
    # directory to save arrays as txt files

    fluxSums = np.zeros((3139,7),dtype=object)
    fluxPeaks = np.zeros((3139,7),dtype=object)

    # (0,i) is total number of data points
    # (1,i) is total number of missing data points

    flare = 0
    totalmissing = 0
    bgnotmin = 0

    keys,tstarts,tpeaks,tfinals = openRibbonDB.openRibbonDB()

    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.txt'):

            data = np.loadtxt(directory+filename,delimiter=',',dtype=float)

            print('flare',flare)

            fluxSums[flare,0] = keys[flare]
            fluxPeaks[flare,0] = keys[flare]

            #for i in range(0,39):
            for i in range(0,6): # use for AIA lines
                lineflux = data[1:,i+1] # 0th column (:,0) is time in SOD of measurement in that row
                # 0th row is a header
                # data file for each event has values of 0 for times outside of event start,end

                missing = 0
                datalength = np.count_nonzero(lineflux) # actual number of data in event
                background = lineflux[0] # AR flux value to be subtracted from flare flux values

                '''
                if not (background == min(lineflux)):
                    bgnotmin +=1
                    linebgnotmin +=1
                    print('no background - zeroing out line in event')
                    for j in range(len(lineflux)):
                        lineflux[j] = 0
                '''
                # above comment block zeros out event if background is not the minimum flux during event

                for j in range(len(lineflux)):
                    if background < 0:
                        bgnotmin +=(1/len(lineflux))
                        lineflux[j] = 0
                    else:
                        lineflux[j] = lineflux[j] - background
                        if lineflux[j] < 0:
                            lineflux[j] = 0
                            missing +=1
                            totalmissing +=1

                fluxSums[0,i+1] = fluxSums[0,i+1] + datalength # total number of nz data points per line for all events
                fluxSums[1,i+1] = fluxSums[1,i+1] + missing # total number of missing data per line for all events
                fluxSums[flare+2,i+1] = sum(lineflux) # total flux value per event for each line

                fluxPeaks[0,i+1] = fluxPeaks[0,i+1] + datalength
                fluxPeaks[1,i+1] = fluxPeaks[1,i+1] + missing
                fluxPeaks[flare+2,i+1] = max(lineflux) # maximum flux value per event for each line

            flare+=1

    print('Total percent of data points missing:',totalmissing/sum(fluxSums[0,:]) * 100)

    for i in range(6):
        print(float(fluxSums[1,i+1] / fluxSums[0,i+1]) * 100,'% missing sum values for line',i)
        print(float(fluxPeaks[1,i+1] / fluxPeaks[0,i+1]) * 100,'% missing peak values for line',i)

    if save == True:
        np.savetxt(directory+'total/AIAFluxSums.txt', fluxSums,fmt = '%1.10f',delimiter=';')
        print('FluxSums saved:', directory + 'total/AIAFluxPeaks.txt')
        np.savetxt(directory+'total/AIAFluxPeaks.txt', fluxPeaks,fmt = '%1.10f',delimiter=';')
        print('FluxPeaks saved:',directory+'total/AIAFlarePeaks.txt')

    print('Total background events not usable:',bgnotmin)

    return fluxSums, fluxPeaks