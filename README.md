# SF_RFI_mask 

Author : Yu Wang

branch : dev

E-mail: ywang@zhejianglab.com 

- This dir contains python code for RFI mitigation by spatial filter (for \*T_bl.fits)
- The main.py calls the other module.
- The config.py contains the paramter for RFI mitigation.
- The spatial_filter.py, read_write.py, baseline_removal.py contain the function for spatial filter, reading and writing the fits file, and the baseline removal, respectively.
- The read_fits.py is used to check the input and output.

-------------
## How to use

1. make sure all the 19-beam data are in the input dir(input_dir).
 
2. edit the config.py

   set 'start_mjd_idx', 'end_mjd_idx', 'start_freq_idx', 'end_freq_idx' 
   
   These four parameters determine the time and frequency range over which the data is processed.
   
   set 'start_freq_lim', 'end_freq_lim', better in the range from start_freq_idx to end_freq_idx.
   
   These two parameters determine the time and frequency range of data used for correction, choose the RFI-free region.
   
   set 'path2save'
   
   The path to save the results, the RFI mitigation data will save in path2save/output dir
   
   The raw and mitigated figure will save in path2save/raw and path2save/clean, respectively.
   
3. run: python mian.py input_dir

-------------

