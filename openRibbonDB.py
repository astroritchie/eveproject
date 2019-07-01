'''



'''

def openRibbonDB():

    import csv as csv

    with open('/Users/kentritchie1/Desktop/KazachenkoResearch/RibbonDB_v1.0/ribbondb_v1.0.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = []
        keys = []
        tstarts = []
        tpeaks = []
        tfinals = []
        for row in reader:
            data.append(row)

        for i in range(1, len(data)):
            key = str(data[i][1])
            tstart = str(data[i][2])
            tpeak = str(data[i][3])
            tfinal = str(data[i][4])

            keys.append(key)
            tstarts.append(tstart)
            tpeaks.append(tpeak)
            tfinals.append(tfinal)

            print(key)

    return key, tstart, tpeak, tfinal