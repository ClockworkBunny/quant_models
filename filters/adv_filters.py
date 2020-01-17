"""
Filters are used to filter the price in time series
"""
import numpy as np
import pandas as pd
from PyEMD import EMD
import pywt
from statsmodels.robust import mad

def _filter_imfs(imfs, threshold):
    """
    This moethod is required by all the bar types and is used to create the desired bars
    """
    num_component = round(imfs.shape[0]*threshold)
    result_seq = np.sum(imfs[num_component:], axis=0)
    return result_seq

def emd_filter(raw_time_series, threshold=0.5):
    """
    This method is required by all the bar types and is used to create the desired bars.
    :params
    1. raw_time_series: (time series in numpy array)
    2. threshold:       (float number)
    it denotes how much low-frequency components will be kept. It should be in the range of [0, 1]

    :return: the same-length data
    """
    # initalize the EMD
    emd = EMD()
    # apply the EMD decomposition
    imfs = emd.emd(raw_time_series)
    # save the low frequent components
    new_time_series = _filter_imfs(imfs, threshold)
    return new_time_series


def wvlet_filter(raw_time_series, wavelet='db4', level=1, title=None):
    """
    wavelet smooth function
    :params
    1. raw_time_series: (time series in numpy array)
    2. wavelet:       type of wavelet (string)
    3. level: cut-off level

    :return: the same-length data
    """
    # calcualte the wavelet coefficients
    coeff = pywt.wavedec(raw_time_series, wavelet, mode="per")
    # calculate a threshold
    sigma = mad(coeff[-level])
    uthresh = sigma * np.sqrt( 2*np.log( len(raw_time_series) ))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode='soft') for i in coeff[1:])
    # reconstruct the signal
    y =  pywt.waverec( coeff, wavelet, mode='per')
    return y


def smooth_algo(arr_in, window, func, kwargs={}):
    """
    wavelet smooth function
    :params
    1. raw_time_series: (time series in numpy array)
    2. wavelet:       type of wavelet (string)
    3. level: cut-off level

    :return: the same-length data
    """
    arr_length = arr_in.shape[0]
    filter_singal = np.copy(arr_in)
    for i in range(window-1, arr_length):
        filter_singal[i] = func(arr_in[i-window+1: i+1], **kwargs)[-1]
    return filter_singal