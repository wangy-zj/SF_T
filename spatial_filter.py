## construct the spatial filter and remove the interference subspace
from sre_constants import _NamedIntConstant
import numpy as np
import config
import torch
import sys


beam = config.beam
start_freq_lim = config.start_freq_lim
end_freq_lim = config.end_freq_lim

## calculate the covariance matrix
def make_covariance_matrix(data):
    l,m,n = data.shape
    D=np.zeros((beam,beam,m,n))
    D_filter=np.zeros((beam,beam,n))
    data_filter = data.mean(axis=1)
    for i in range(beam):
        for j in range(beam):
            D[i][j] = np.sqrt(data[i]*data[j])
            D_filter[i][j] = np.sqrt(data_filter[i]*data_filter[j])
    D_ms = np.transpose(D,(2,3,0,1)).astype('float32')
    D_filter = np.transpose(D_filter,(2,0,1)).astype('float32')
    return D_ms,D_filter       

## Eigen decomposition of the covariance matrix
def subspace_projection(data):
    D_ms,D_filter = make_covariance_matrix(data)
    l,m,n = data.shape
    data_clean = np.zeros_like(data)
    rfi_components = 1
    correlation_cpu = torch.tensor(D_filter)
    u_cpu, _, _ = torch.linalg.svd(correlation_cpu)
    rfi_eigenvector = np.array(u_cpu)

    ### subject the RFI subspace ###
    spectrum = np.zeros([m,n,beam])
    for i in range(m):
        for j in range(n):
            u_sample = rfi_eigenvector[int(j)].squeeze()
            u_rfi = u_sample[:,:rfi_components]
            P = np.dot(u_rfi,u_rfi.T)
            c = D_ms[i][j]
            matrix_clean = c - np.dot(P,np.dot(c,P))
            spectrum[i][j] = np.diag(matrix_clean)
    spectrum = np.transpose(spectrum,(2,0,1))
    for k in range(beam):
        data_clean[k]=spectrum[k]
    data_clean[data_clean<0]=0
    return data_clean


def baseline_removal(data):
    for i in range(beam):
        baseline = data[i,:,start_freq_lim:end_freq_lim].mean(axis=-1)
        baseline = baseline.mean(axis=-1)
        data[i] = data[i,:,:] - baseline
    return data
