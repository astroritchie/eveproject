'''
Author: Kent Ritchie - last updated 2/23/19

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
fluxarray = getEVLflux('2010-06-12 00:30','2010-06-12 01:02', True)

'''


import datetime as dt
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

def getEVLflux(tstart,tfinal,savetxt,savename):
    
    start_year = int(tstart[0:4])
    start_month = int(tstart[5:7])
    start_day = int(tstart[8:10])
    start_hour = int(tstart[11:13])
    if start_hour < 10:
        start_hour = '0' + str(start_hour)
    start_minute = int(tstart[15:17])
    
    #print('year:',start_year)
    #print('month:',start_month)
    #print('day:',start_day)
    #print('hour:',start_hour)
    #print('min:',start_minute)
    
    final_year = int(tfinal[0:4])
    final_month = int(tfinal[5:7])
    final_day = int(tfinal[8:10])
    final_hour = int(tfinal[11:13])
    if final_hour < 10:
        final_hour = '0' + str(final_hour)
    final_minute = int(tfinal[15:17])
    
    
    start_doy = (dt.date(start_year, start_month, start_day) - dt.date(start_year,1,1)).days + 1
    end_doy = (dt.date(final_year, final_month, final_day) - dt.date(final_year,1,1)).days + 1
    
    # need to consider if the year changes i.e. flare lasting 12/31 -> 1/1
    
    if start_doy == end_doy:
        nfiles = int(final_hour) - int(start_hour) + 1
    
        if int(final_hour) - int(start_hour) == 0:
            nfiles = 1
            
    else:
        nfiles = np.abs((24 - int(start_hour)) + int(final_hour)) # this assumes the maximum doy difference is 1
    
    filenum = np.arange(0,nfiles,1)
    linenum = np.arange(0,39,1)
    timenum = np.arange(0,360,1)
    EVLfiles = []
    flux = np.empty(39,dtype=object)
    sod = np.empty(360*nfiles,dtype=float)

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
            lineflux = np.asarray(data[:,j])
            
            if i == 0:
                flux[j] = lineflux[:]
            else:
                flux[j] = np.append(flux[j],lineflux)
            
        for k in timenum:
            timeval = times[k]
            sod[k+(i*360)] = timeval
            
    fluxtimearray = [flux,sod]

    if savetxt == True:    
        np.savetxt('/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/FlareTxtFiles/%s.txt' % savename, fluxtimearray,fmt = '%s')

    return fluxtimearray