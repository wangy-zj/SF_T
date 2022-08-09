# config the parameters for ArPLS-SF
import numpy as np

debug = True

## the input raw data size
obs_mode = 'arcdrift'
beam = 19                

## parameters of the spatial filter
pol_num = -2   #the pol number to process 0 means XX,1 means YY, -1 means process XX,YY independently, and -2 means XX+YY

##time and frequency range to process
start_mjd_idx = -800
end_mjd_idx = -1
start_freq_idx = 13400
end_freq_idx = 14000

### time and frequency range to 
start_mjd_lim = 0
end_mjd_lim = -1
start_freq_lim = 13600
end_freq_lim = 13800
start_freq_lim = start_freq_lim - start_freq_idx
end_freq_lim = end_freq_lim - end_freq_idx

results = 'clean'  
'''
'clean' or 'flag'
if results='clean' the results only output the filtered data
if results='flag' the results include the mask file
'''

## path to save the results
path2save = '/home/wangy/SF_test/results/0160/'

