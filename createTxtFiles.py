'''

Create txt files for every flare event in RibbonDB

Method:

1. Look in RibbonDB
2. Grab tstart and tfinal
3. get flux as function of time for each line
4. Create and save txt file for each event of flux array

'''

import getEVLflux
import csv as csv

def createTxtFiles():
    with open('/Users/kentritchie1/Desktop/KazachenkoResearch/RibbonDB_v1.0/ribbondb_v1.0.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            data = []
            for row in reader:
                data.append(row)

            for i in range(1,len(data)):
                key = str(data[i][1])
                tstart = str(data[i][2])
                tpeak = str(data[i][3])
                tfinal = str(data[i][4])

                getEVLflux(tstart,tfinal,True,key)