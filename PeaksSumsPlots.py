'''

Plot peak flare values for specific line

'''

import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy import stats

directory = '/Users/kentritchie1/Desktop/KazachenkoResearch/EVE_project/FlareTxtFiles/total/'


sums = np.loadtxt(directory+'FlareSums.txt',delimiter=';',dtype=np.float)
peaks = np.loadtxt(directory+'FlarePeaks.txt',delimiter=';',dtype=np.float)

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
        
        vals = [ val for val in peaks[:,i] if val > 0]

        plt.figure(figsize=(14,8))
        plt.scatter(phi_rbn,peaks[:,i],marker='.')
        plt.ylim(0.95*min(vals),1.05*max(vals))
        plt.xscale('log')
        plt.yscale('log')
        plt.title('Peak Flux vs Reconnection Flux\n%s' % wavelengths[i])
        plt.xlabel('Total Unsigned Flare-Ribbon Reconnection Flux [MX]')
        plt.ylabel('Peak Flux [W/M^2]')
        plt.grid()
        plt.show()
        
        vals = [ val for val in sums[:,i] if val > 0]

        plt.figure(figsize=(14,8))
        plt.scatter(phi_rbn,sums[:,i],marker='.')
        plt.ylim(0.95*min(vals),1.05*max(vals))
        plt.xscale('log')
        plt.yscale('log')
        plt.title('Total Flux vs Reconnection Flux\n%s' % wavelengths[i])
        plt.xlabel('Total Unsigned Flare-Ribbon Reconnection Flux [MX]')
        plt.ylabel('Total Flux [W/M^2]')
        plt.grid()
        plt.show()