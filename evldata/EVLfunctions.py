
'''
Collection of Python scripts for SDO EVL data analysis pertaining to RibbonDB

Author: Kent Ritchie; National Solar Observatory; Boulder, CO

Updates:
    7/11/19 - created master module

To-do:
    Add in all functions
'''





'''
openRibbonDB
'''

def openRibbonDB():

    import csv

    with open('/Users/kentritchie1/Desktop/KazachenkoResearch/RibbonDB_v1.0/ribbondb_v1.0.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in reader:
            data.append(row)

        keys = []
        tstart = []
        tpeak = []
        tfinal = []

        for i in range(1, len(data)):
            keys.append(str(data[i][1]))
            tstart.append(str(data[i][2]))
            tpeak.append(str(data[i][3]))
            tfinal.append(str(data[i][4]))

    return keys, tstart, tpeak, tfinal





'''
Author: Kent Ritchie - last updated 7/11/19
Purpose: Creates txt file of flux and time values for a single flare event
Function: getEVLflux(tstart,tfinal)
Parameters:
tstart: string of RibbonDB tstart with RibbonDB naming convention
tfinal: string of RibbonDB tfinal with RibbonDB naming convention
savetxt: True or False
Returns:
flux: flux values for all EVE lines from tstart to tfinal as an array of shape (0,39)
        Each element of the array contains all flux values for that emission line of size nfiles
        where nfiles = number of hours (therefor files) for flare event duration

sod: seconds of day for each EVE line measurement as an array of shape (0,360*nfiles)
if savetxt == True: saves .txt file of array where array[0] = flux, array[1] = sod
Usage:
fluxarray = getEVLflux(' 2010-06-12 00:30',' 2010-06-12 01:02', True)
'''

def getEVLflux(tstart, tfinal, savetxt, savename):

    import datetime as dt
    from astropy.io import fits
    import numpy as np

    start_year = int(tstart[1:5])
    start_month = int(tstart[6:8])
    start_day = int(tstart[9:11])
    start_hour = int(tstart[12:14])
    if start_hour < 10:
        start_hour = '0' + str(start_hour)
    start_minute = int(tstart[15:17])
    if start_minute < 10:
        start_minute = '0' + str(start_minute)

    start_sod = float((int(start_hour) * 3600) + (int(start_minute) * 60))

    final_year = int(tfinal[1:5])
    final_month = int(tfinal[6:8])
    final_day = int(tfinal[9:11])
    final_hour = int(tfinal[12:14])
    if final_hour < 10:
        final_hour = '0' + str(final_hour)
    final_minute = int(tfinal[15:17])
    if final_minute < 10:
        final_minute = '0' + str(final_minute)

    final_sod = float((int(final_hour) * 3600) + (int(final_minute) * 60))

    start_doy = (dt.date(start_year, start_month, start_day) - dt.date(start_year, 1, 1)).days + 1
    end_doy = (dt.date(final_year, final_month, final_day) - dt.date(final_year, 1, 1)).days + 1

    # need to consider if the year changes i.e. flare lasting 12/31 -> 1/1

    if start_doy == end_doy:
        nfiles = int(final_hour) - int(start_hour) + 1

        if int(final_hour) - int(start_hour) == 0:
            nfiles = 1

    else:
        nfiles = np.abs((24 - int(start_hour)) + int(final_hour))  # this assumes the maximum doy difference is 1

    filenum = np.arange(0, nfiles, 1)
    linenum = np.arange(0, 39, 1)
    EVLfiles = []
    fluxtime = np.empty((360 * nfiles, 40), dtype=float)

    for i in filenum:
        if i == 0:
            file_hour = start_hour
        else:
            file_hour = int(start_hour) + int(i)

        if int(start_doy) < 10:
            start_doy = '00' + str(int(start_doy))

        if int(start_doy) > 9 and int(start_doy) < 100:
            start_doy = '0' + str(int(start_doy))

        if int(file_hour) < 10:
            file_hour = str('0') + str(int(file_hour))

        file_doy = start_doy

        if int(file_hour) > 23:
            file_hour = int(file_hour) - 24
            file_doy = str(int(start_doy) + 1)

            if int(file_doy) < 10:
                file_doy = '00' + str(int(file_doy))

            if int(file_doy) > 9 and int(file_doy) < 100:
                file_doy = '0' + str(int(file_doy))

            if int(file_hour) < 10:
                file_hour = str('0') + str(int(file_hour))

        EVLfile = 'EVL_L2_' + str(start_year) + str(file_doy) + '_' + str(file_hour) + '_006_02.fits'
        EVLfiles.append(EVLfile)

        current_file = '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/EVE_data/' + EVLfile

        hdul = fits.open(current_file)
        linesdata = hdul['LinesData'].data
        data = linesdata['Line_Irradiance']
        times = linesdata['SOD']

        for j in linenum:
            lineflux = data[:, j]
            fluxtime[i * 360:360 + (i * 360), j + 1] = lineflux

        for k in range(0, len(times)):
            timeval = times[k]

            if not (start_sod <= timeval <= final_sod):
                fluxtime[k + (i * 360), :] = 0

            else:
                fluxtime[k + (i * 360), 0] = timeval

    if savetxt == True:
        np.savetxt('/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/FlareTxtFiles/%s.txt' % savename,
            fluxtime, fmt='%1.10f', delimiter=',')

    return fluxtime





'''
createTxtFiles
'''

def createTxtFiles():

    import getEVLflux
    import openRibbonDB

    count = 0

    keys,tstart,tpeak,tfinal = openRibbonDB()

    for i in range(0,len(keys)):
        getEVLflux(tstart[i],tfinal[i],True,keys[i])
        count += 1

    print(count,'txt files created')





'''
Author: Kent Ritchie
Purpose: Calculate total flux and peak flux values for each flare event in RibbonDB per 39 emission lines
Function: calcSumPeak()
Parameters: None
Needs: 3137 .txt files corresponding to flux information for each flare event in RibbonDB as created by createTxtFiles()
numpy, os libraries
Subfunction Invocations: None
Returns: None
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

def calcSumPeak():

    import numpy as np
    import os

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





'''
Author: Kent Ritchie

Purpose: Calculate total flux and peak flux values for each flare event in RibbonDB for AIA emission lines
         Same function as calcSumPeak but for AIA lines only

Function: calcAIASumPeak()

Parameters: 
    save: if True will save .txt files as formatted below in Saves description

Needs: 3137 .txt files corresponding to flux information for each flare event in RibbonDB as created by createTxtFiles()
       numpy, os libraries

Subfunction Invocations: None

Returns: fluxSums, fluxPeaks arrays

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





'''
Download EVE L2 files for all RibbonDB flares
Method:
1. Look in RibbonDB
2. Grab tstart and tfinal
3. Create list of EVE L2 files from tstart and tfinal
4. Download each EVE L2 file with urllib.request.urlretrieve
'''
def listofEVEfiles():

    import csv
    import urllib.request

    listoffiles = []

    with open('/Users/kentritchie1/Desktop/KazachenkoResearch/RibbonDB_v1.0/ribbondb_v1.0.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in reader:
            data.append(row)

        flarecount = 0
        filecount = 0

        for i in range(1, len(data)):
            key = str(data[i][1])
            tstart = str(data[i][2])
            tpeak = str(data[i][3])
            tfinal = str(data[i][4])

            start_year = int(tstart[1:5])
            start_month = int(tstart[6:8])
            start_day = int(tstart[9:11])
            start_hour = int(tstart[12:14])
            if start_hour < 10:
                start_hour = '0' + str(start_hour)
            start_minute = int(tstart[16:18])

            final_year = int(tfinal[1:5])
            final_month = int(tfinal[6:8])
            final_day = int(tfinal[9:11])
            final_hour = int(tfinal[12:14])
            if final_hour < 10:
                final_hour = '0' + str(final_hour)
            final_minute = int(tfinal[16:18])

            start_doy = (dt.date(start_year, start_month, start_day) - dt.date(start_year, 1, 1)).days + 1

            end_doy = (dt.date(final_year, final_month, final_day) - dt.date(final_year, 1, 1)).days + 1

            # need to consider if the year changes i.e. flare lasting 12/31 -> 1/1

            if start_doy == end_doy:
                nfiles = int(final_hour) - int(start_hour) + 1

                if int(final_hour) - int(start_hour) == 0:
                    nfiles = 1

            else:
                nfiles = np.abs(
                    (24 - int(start_hour)) + int(final_hour))  # this assumes the maximum doy difference is 1

            filenum = np.arange(0, nfiles, 1)

            for i in filenum:

                if i == 0:
                    file_hour = start_hour
                else:
                    file_hour = int(start_hour) + int(i)

                if int(start_doy) < 10:
                    start_doy = '00' + str(int(start_doy))

                if int(start_doy) > 9 and int(start_doy) < 100:
                    start_doy = '0' + str(int(start_doy))

                if int(file_hour) < 10:
                    file_hour = str('0') + str(int(file_hour))

                file_doy = start_doy

                if int(file_hour) > 23:
                    file_hour = int(file_hour) - 24
                    file_doy = str(int(start_doy) + 1)

                    if int(file_doy) < 10:
                        file_doy = '00' + str(int(file_doy))

                    if int(file_doy) > 9 and int(file_doy) < 100:
                        file_doy = '0' + str(int(file_doy))

                    if int(file_hour) < 10:
                        file_hour = str('0') + str(int(file_hour))

                EVLfile = 'EVL_L2_' + str(start_year) + str(file_doy) + '_' + str(file_hour) + '_006_02.fit.gz'

                # print(key,EVLfile)

                listoffiles.append(EVLfile)

                url = 'http://lasp.colorado.edu/eve/data_access/evewebdataproducts/level2/%s/%s/%s' % (
                start_year, file_doy, EVLfile)

                print(url)

                urllib.request.urlretrieve(url,
                                           '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/EVE_data/%ss' % EVLfile[
                                                                                                                       0:-3])

                filecount += 1

            flarecount += 1

    print(flarecount, 'flares')
    print(filecount, 'files')

    return listoffiles






'''
Plot peak flare values for specific line
'''

def makeplots()

    import numpy as np
    import csv
    import matplotlib.pyplot as plt
    from scipy import stats

    directory = '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/FlareTxtFiles/total/'


    sums = np.loadtxt(directory+'bgsFlareSums.txt',delimiter=';',dtype=np.float)
    peaks = np.loadtxt(directory+'bgsFlarePeaks.txt',delimiter=';',dtype=np.float)
    '''
    for i in range(0,20):
        print(sums[i][0:39])
    '''
    #Plotting

    with open('/Users/kentritchie1/Desktop/KazachenkoResearch/RibbonDB_v1.0/ribbondb_v1.0.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in reader:
            data.append(row)

        ixpeak = []
        phi_rbn = []
        dphi_rbn = []

        for i in range(1,len(data)):
            ixpeak.append(data[i][5])
            phi_rbn.append(data[i][10])
            dphi_rbn.append(data[i][11])

        ixpeak = np.asarray(ixpeak,dtype='float')
        phi_rbn = np.asarray(phi_rbn,dtype='float')
        dphi_rbn = np.asarray(dphi_rbn,dtype='float')

        wavelengths = [
            'Fe XVIII 9.39260nm','Fe VIII 13.1240nm','Fe XX 13.2850nm','Fe IX 17.1070nm',
            'Fe X 17.7243nm','Fe XI 18.0407nm','Fe XII 19.5120nm','Fe XIII 20.2044nm',
            'Fe XIV 21.1331nm','He II 25.6317nm','Fe XV 28.4150nm','He II 30.3783nm',
            'Fe XVI 33.5410nm','Fe XVI 36.0758nm','Mg IX 36.8076nm','S XIV 44.5700nm',
            'Ne VII 46.5221nm','Si XII 49.9406nm','Si XII 52.1000nm','O III 52.5795nm',
            'He I 53.7000nm','O IV 55.4370nm','Fe XX 56.7870nm','He I 58.4334nm',
            'Fe XIX 59.2240nm','O III 59.9598nm','Mg X 60.9800nm','Mg X 62.4943nm',
            'O V 62.9730nm','O II 71.8535nm','Fe XX 72.1560nm','Ne VIII 77.0409nm',
            'O IV 79.0199nm','O II 83.5500nm','H I 94.9700nm','H I 97.2537nm',
            'C III 97.7030nm','H I 102.572nm','O VI 103.190nm'
        ]



        for i in range(0,39):

            vals = [ val for val in peaks[2:,i] if val > 0 ]#and val < 1]

            plt.figure(figsize=(14,8))
            plt.scatter(phi_rbn,peaks[2:,i],marker='.')
            plt.ylim(0.95*min(vals),1.05*max(vals))
            plt.xscale('log')
            plt.yscale('log')
            plt.title('Peak Flux vs Reconnection Flux\n%s\nPercent of Values Missing/Corrupt:%3d %%' % (wavelengths[i],(peaks[1,i]/peaks[0,i])*100))
            plt.xlabel('Total Unsigned Flare-Ribbon Reconnection Flux [MX]')
            plt.ylabel('Peak Flux [W/M^2]')
            plt.grid()
            #plt.show()
            plt.savefig('/Users/kentritchie1/Desktop/KazachenkoResearch/eveproject/plots/bgspeakflux_%s.pdf' % (wavelengths[i].strip()),dpi=500)
            #plt.close()

            #print(sums[:,i])

            vals = [ val for val in sums[2:,i] if val > 0 ]#and val < 1]

            plt.figure(figsize=(14,8))
            plt.scatter(phi_rbn,sums[2:,i],marker='.')
            plt.ylim(0.9*min(vals),1.1*max(vals))
            plt.xscale('log')
            plt.yscale('log')
            plt.title('Total Flux vs Reconnection Flux\n%s\nPercent of Values Missing/Corrupt:%3d %%' % (wavelengths[i],(sums[1,i]/sums[0,i])*100))
            plt.xlabel('Total Unsigned Flare-Ribbon Reconnection Flux [MX]')
            plt.ylabel('Total Flux [W/M^2]')
            plt.grid()
            #plt.show()
            plt.savefig('/Users/kentritchie1/Desktop/KazachenkoResearch/eveproject/plots/bgstotalflux_%s.pdf' % (wavelengths[i].strip()),dpi=500)
            #plt.close()

        for i in range(39):
            print('Line %s %s: Missing %3d%%\n' % (i, wavelengths[i] , (peaks[1,i]/peaks[0,i])*100))






'''
'''