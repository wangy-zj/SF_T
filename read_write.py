from tabnanny import filename_only
import astropy.io.fits as pyfits
import numpy as np
import matplotlib.pyplot as plt
import os,sys,glob
from threading import Lock, Thread
from decimal import Decimal
from copy import copy
import threading

import config

lock = threading.Lock()
beam = config.beam
start_chan_idx = config.start_freq_idx
end_chan_idx = config.end_freq_idx
start_mjd_idx = config.start_mjd_idx
end_mjd_idx = config.end_mjd_idx

### Functions to plot both the waterfull and the integrated spectrum figure ###
'''
input:
data: the 2-D data to plot
filename,source_name: the raw data filename and source name used to generate the figure's name
'''
### plot the raw fits data
def plot_raw(data,filename,source_name):
    l,m=data.shape
    fig=plt.figure()
    basename = filename[filename.find(source_name):filename.find('.fits')]
    plt.imshow(data,
            aspect='auto',
            rasterized=True,
            interpolation='nearest',
            cmap='hot',extent=(0,m,0,l),
        )
    figure_name = config.path2save + 'raw/' + basename + '_raw' + '.png'
    plt.xlabel("Channel")
    plt.ylabel("Time")
    plt.title(basename)
    plt.colorbar()
    plt.savefig(figure_name,dpi=400)
    plt.close()

    plt.plot(data.mean(axis=0),linewidth=0.7)
    plt.xlabel('Channel')
    figure_name_spec = config.path2save + 'raw/' + basename + '_raw_avg.png'
    plt.savefig(figure_name_spec,dpi=400)
    plt.close()

### plot the data after baseline removal 
def plot_baseline(data,filename,source_name):
    l,m=data.shape
    #f_xticks = f_arr_process.astype('int')
    fig=plt.figure()
    basename = filename[filename.find(source_name):filename.find('.fits')]
    plt.imshow(data,
            aspect='auto',
            rasterized=True,
            interpolation='nearest',
            cmap='hot',extent=(0,m,0,l),
        )
    figure_name = config.path2save + 'baseline/' + basename + '_baseline_removal' + '.png'
    plt.xlabel("Channel")
    #plt.xticks(np.arange(0,len(f_arr_process),len(f_arr_process)//5),f_xticks[::len(f_arr_process)//5])
    plt.ylabel("Time")
    plt.title(basename)
    plt.colorbar()
    plt.savefig(figure_name,dpi=400)
    plt.close()

    plt.plot(data.mean(axis=0),linewidth=0.7)
    plt.xlabel('Channel')
    #plt.xticks(np.arange(0,len(f_arr_process),len(f_arr_process)//5),f_xticks[::len(f_arr_process)//5])
    figure_name_spec = config.path2save + 'baseline/' + basename + '_baseline_removal_avg.png'
    plt.savefig(figure_name_spec,dpi=400)
    plt.close()

### plot the data after spatial filter
def plot_clean(data,filename,source_name):
    l,m=data.shape
    #f_xticks = f_arr_process.astype('int')
    fig=plt.figure()
    basename = filename[filename.find(source_name):filename.find('.fits')]
    plt.imshow(data,
            aspect='auto',
            rasterized=True,
            interpolation='nearest',
            cmap='hot',extent=(0,m,0,l),
        )
    figure_name = config.path2save + 'clean/' + basename + '_clean' + '.png'
    plt.xlabel("Channel")
    #plt.xticks(np.arange(0,len(f_arr_process),len(f_arr_process)//5),f_xticks[::len(f_arr_process)//5])
    plt.ylabel("Time")
    plt.title(basename)
    plt.colorbar()
    plt.savefig(figure_name,dpi=400)
    plt.close()
    
    #plt.plot(f_arr.squeeze(),data.mean(axis=0),linewidth=0.7)
    plt.plot(data.mean(axis=0),linewidth=0.7)
    plt.xlabel('Channel')
    #plt.xticks(np.arange(0,len(f_arr_process),len(f_arr_process)//5),f_xticks[::len(f_arr_process)//5])
    figure_name_spec = config.path2save + 'clean/' + basename + '_clean_spec_avg.png'
    plt.savefig(figure_name_spec,dpi=400)
    plt.close()


### write the mask file and plot the figure (multiprocess)
def out(d_clean,filename,source_name):
    data = read_fit_T(filename)
    if config.pol_num==-2:
        plot_raw(data.mean(axis=-1),filename,source_name)
        #plot_baseline(data_baseline,filename,source_name)
        plot_clean(d_clean.mean(axis=-1),filename,source_name)
    else:
        plot_raw(data,filename,source_name)
        #plot_baseline(data_baseline,filename,source_name)
        plot_clean(d_clean,filename,source_name)        
    
    hdu = pyfits.open(filename)
    hdu[0].data = hdu[0].data[start_chan_idx:end_chan_idx]
    hdu[1].data = hdu[1].data[start_mjd_idx:end_mjd_idx]
    hdu[2].data = d_clean
    save_filename = config.path2save + 'output/' + filename[filename.find(source_name):]
    file = open(save_filename,'wb')
    hdu.writeto(save_filename,overwrite=True)
    file.close()
    


def read_fit_T(filename,type='process'):
    if os.path.splitext(filename)[-1]=='.fits':
        hdulist = pyfits.open(filename)
        hdu1 = hdulist[2]
        data = hdu1.data
        if config.pol_num == -2:
            data_process = data[start_mjd_idx:end_mjd_idx,start_chan_idx:end_chan_idx,:]
        elif config.pol_num == -1:
            data_process = data[start_mjd_idx:end_mjd_idx,start_chan_idx:end_chan_idx,:].mean(axis=-1).squeeze()
        else:
            data_process = data[start_mjd_idx:end_mjd_idx,start_chan_idx:end_chan_idx,config.pol_num]
    return data_process

### read the 19-beam fits files one by one
def read_fits(path):
    fileList = sorted(glob.glob(path+'*.fits')) #read 19 beam fits data into data(19,T_sample,F_sample)
    data=[]
    f_name=[]
    for i in range(beam):
        data.append(read_fit_T(fileList[i]))
        f_name.append(fileList[i])
    data=np.array(data)
    return data,f_name
    
