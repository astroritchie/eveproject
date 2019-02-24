'''
Kent Ritchie
Pre-Interview
RibbonDB Reconnection Flux Plot
'''
import csv
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

with open('/Users/kentritchie1/Desktop/KazachenkoResearch/RibbonDB_v1.0/ribbondb_v1.0.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    data = []
    for row in reader:
        data.append(row)
        
    ixpeak = []
    phi_rbn = []
    dphi_rbn = []
    
    key = []
    tstart = []
    tpeak = []
    tfinal = []
    lat = []
    long = []
    arnum = []
    phi_ar = []
    s_ar = []
    s_rbn = []
    ds_rbn = []
    r_phi = []
    r_s = []
    
    for i in range(1,len(data)):
        ixpeak.append(data[i][5])
        phi_rbn.append(data[i][10])
        dphi_rbn.append(data[i][11])
        
    ixpeak = np.asarray(ixpeak,dtype='float')
    phi_rbn = np.asarray(phi_rbn,dtype='float')
    dphi_rbn = np.asarray(dphi_rbn,dtype='float')

plt.figure(figsize=(14,8))

color = np.log10(ixpeak)
plt.scatter(phi_rbn,ixpeak,marker='.',c=color)
plt.title('Peak X-Ray Flux vs Reconnection Flux')
plt.xlabel('Total Unsigned Flare-Ribbon Reconnection Flux [MX]')
plt.ylabel('Peak 1-8A X-Ray Flux [W/M^2]')
plt.xscale('log')
plt.yscale('log')
plt.ylim((1e-6,1e-3))
plt.grid()
cbar = plt.colorbar(pad=0)
cbar.set_label("Log10 Peak X-Ray Flux", labelpad=+10)
plt.clim(-6,-3) 
cbar.set_ticks([-6,-5,-4,-3])
cbar.set_ticklabels(['-6','-5','-4','-3'])
plt.show()
#plt.savefig('/Users/kentritchie1/Desktop/XRay_vs_ReconnectionFlux.pdf',dpi=500)