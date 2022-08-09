# -*- coding: UTF-8 -*- 
from importlib.resources import path
import time
import os,sys
from threading import Thread
import numpy as np
import warnings

import config
import spatial_filter as sf
import read_write as rw
import baseline_removal

warnings.filterwarnings('ignore')

### main code ###
if __name__=='__main__':
    time_start = time.time()
    beam = config.beam
    filepath = sys.argv[1]

    if not os.path.exists(config.path2save):
        os.mkdir(config.path2save)
        os.mkdir(config.path2save+'/raw')
        os.mkdir(config.path2save+'/baseline')
        os.mkdir(config.path2save+'/clean')
        os.mkdir(config.path2save+'/output')
        if config.results =='flag':
            os.mkdir(config.path2save+'/mask')

	
    ### read the original fits files
    data,filename = rw.read_fits(filepath)

    if filename[0].find(config.obs_mode) != -1:
        source_name = filename[0][filename[0].find('/Dec'):filename[0].find('_'+config.obs_mode)][1:]
        print('Observation name:',source_name)
    else:
        sys.exit('Wrong observation mode!')

    ### baseline removal
    #data_baseline = baseline_removal.baseline_removal(data)
    data = data + 10
    data_baseline = data
    if config.debug:
        print('data_process shape is :',data_baseline.shape,', data type is:',data_baseline.dtype)

    ### spatial filter
    if config.pol_num == -2:
        d_clean = np.zeros_like(data)
        d_clean0 = sf.subspace_projection(data_baseline[:,:,:,0])
        d_clean[:,:,:,0] = sf.baseline_removal(d_clean0)
        d_clean1 = sf.subspace_projection(data_baseline[:,:,:,1])
        d_clean[:,:,:,1] = sf.baseline_removal(d_clean1)
    else:
        d_clean = sf.subspace_projection(data_baseline)
        d_clean = sf.baseline_removal(d_clean)
    if config.debug:
        print('d_clean shape is : ', d_clean.shape,'data type is:',d_clean.dtype)

    ### output
    for i in range(beam):
        rw.out(d_clean[i],filename[i],source_name)

