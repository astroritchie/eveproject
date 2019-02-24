'''

Download EVE L2 files for all RibbonDB flares

Method:

1. Look in RibbonDB
2. Grab tstart and tfinal
3. Create list of EVE L2 files from tstart and tfinal
4. Download each EVE L2 file with urllib.request.urlretrieve

'''
import csv
import urllib.request

def listofEVEfiles():
    
    listoffiles = []

    with open('/Users/kentritchie1/Desktop/KazachenkoResearch/RibbonDB_v1.0/ribbondb_v1.0.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in reader:
            data.append(row)
            
        flarecount = 0
        filecount = 0

        for i in range(1,len(data)):
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

                #print(key,EVLfile)
                
                listoffiles.append(EVLfile)
                
                url = 'http://lasp.colorado.edu/eve/data_access/evewebdataproducts/level2/%s/%s/%s' % (start_year,file_doy,EVLfile)
    
                print(url)
    
                urllib.request.urlretrieve(url,'/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/EVE_data/%ss' % EVLfile[0:-3])
                
                filecount +=1
        
            flarecount += 1

    
    print(flarecount,'flares')
    print(filecount,'files')
    
    return listoffiles