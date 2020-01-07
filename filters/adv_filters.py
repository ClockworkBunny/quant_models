"""
Filters are used to filter the price in time series
"""
import numpy as np
import pandas as pd
from PyEMD import EMD

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
