from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import sys
import config


def read_results(filename):
    hdu = fits.open(filename)
    freq = hdu[0].data
    mjd = hdu[1].data
    data = hdu[2].data
    return freq,mjd,data

def read_data(filename):
    hdu = fits.open(filename)
    freq = hdu[0].data[config.start_freq_idx:config.end_freq_idx]
    mjd = hdu[1].data[config.start_mjd_idx:config.end_mjd_idx]
    data = hdu[2].data[config.start_mjd_idx:config.end_mjd_idx,config.start_freq_idx:config.end_freq_idx,:].mean(axis=-1).squeeze()
    return freq,mjd,data

filename1 = 'results/AGC002272/output/Dec+2715_arcdrift-M01_W_0080_T_bl.fits'
filename2 = 'results/AGC002272/output/Dec+2715_arcdrift-M04_W_0080_T_bl.fits'
#freq1,mjd1,data1 = read_results(filename1)
#freq2,mjd2,data2 = read_results(filename2)


filename3 = 'data/0160/Dec+2715_arcdrift-M02_W_0160_T_bl.fits'
freq,mjd,data = read_data(filename3)

fig = plt.figure(figsize=(12,10))
plt.imshow(data,
        aspect='auto',
        rasterized=True,
        interpolation='nearest',
        cmap='hot',
        #extent=(freq[0],freq[-1],mjd[-1],mjd[0]),
    )
#plt.axhline(y=58892.42373148,color='k',linewidth=0.5)
#f_xticks = freq.astype('int')
#plt.xticks(np.arange(0,len(freq),len(freq)//5),f_xticks[::len(freq)//5])
plt.colorbar()
plt.savefig('test.png',dpi=400)
plt.close()


'''
#plt.plot(freq,(data).mean(axis=0),'r',linewidth=0.7)
plt.plot(freq1,data1.mean(axis=0),'k',linewidth=0.5)
plt.plot(freq2,data2.mean(axis=0),'r',linewidth=0.5)
#plt.plot(freq2,(data2-data1).mean(axis=0),'r',linewidth=0.5)
plt.savefig('test_avg.png',dpi=400)
plt.close()
'''

