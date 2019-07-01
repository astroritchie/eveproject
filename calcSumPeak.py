'''
Author:
Kent Ritchie

Purpose:
Calculate total flux and peak flux values for each flare event in RibbonDB per 39 emission lines

Function:
calcSumPeak()

Parameters:
None

Needs:
3137 .txt files corresponding to flux information for each flare event in RibbonDB as created by createTxtFiles()
numpy, os libraries

Subfunction Invocations:
None

Returns:
None

Saves:
2 separate .txt files, 1 containing total flux values and 1 containing peak flux values
Both .txt files contain the total number of data points and total number of missing data points

Both .txt files have shape (3139,39) where:
Rows correspond to the 39 EVE emission lines
0th column contains number of data points for respective line
1st column contains number of missing data points for respective line
2nd-3139th columns contain either total flux or peak flux values for each event per respective line

Updates:
6-28-19: Removed loop to zero out event if background != min flux val
6-29-19: Made into standalone function via Pycharm
'''

import numpy as np
import os

def calcSumPeak():

    directory = '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/AIALinesFluxTxtFiles/'

    allSums = np.zeros((3139,6),dtype=np.float64)
    allPeaks = np.zeros((3139,6),dtype=np.float64)

    # (0,i) is total number of data points
    # (1,i) is total number of missing data points

    flare = 0
    totalmissing = 0
    bgnotmin = 0

    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.txt'):

            data = np.loadtxt(directory+filename,delimiter=',',dtype=float)

            print('flare',flare)

            for i in range(0,39):
                lineflux = data[1:,i+1] # 0th column (:,0) is time in SOD of measurement in that row
                # 0th row is a header
                # data file for each event has values of 0 for times outside of event start,end

                missing = 0

                linebgnotmin = 0

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

                allSums[0,i] = allSums[0,i] + datalength # total number of nz data points per line for all events
                allSums[1,i] = allSums[1,i] + missing # total number of missing data per line for all events
                allSums[flare+2,i] = sum(lineflux) # total flux of all events per line

                allPeaks[0,i] = allPeaks[0,i] + datalength
                allPeaks[1,i] = allPeaks[1,i] + missing
                allPeaks[flare+2,i] = max(lineflux) # maximum flux value per event for each line

            flare+=1

    print('Total percent of data points missing:',totalmissing/sum(allSums[0,:]) * 100)

    for i in range(6):
        print(float(allSums[1,i] / allSums[0,i]) * 100,'% missing sum values for line',i)
        print(float(allPeaks[1,i] / allPeaks[0,i]) * 100,'% missing peak values for line',i)

    np.savetxt(directory+'total/bgsFlareSums.txt', allSums,fmt = '%1.10f',delimiter=';')
    np.savetxt(directory+'total/bgsFlarePeaks.txt', allPeaks,fmt = '%1.10f',delimiter=';')

    print('Total background events not usable:',bgnotmin)