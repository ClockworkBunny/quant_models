"""
This module is designed for smooth
"""

# Imports
import numpy as np
from numba import jit
from numba import float64
from numba import int64
import pywt
from statsmodels.robust import mad

def waveletSmooth(x, wavelet='db4', level=1, title=None):
    """
    wavelet smooth function
    """
    # calcualte the wavelet coefficients
    coeff = pywt.wavedec(x, wavelet, mode="per")
    # calculate a threshold
    sigma = mad(coeff[-level])
    uthresh = sigma * np.sqrt( 2*np.log( len(x) ))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode='soft') for i in coeff[1:])
    # reconstruct the signal
    y =  pywt.waverec( coeff, wavelet, mode='per')
    return y

@jit((float64[:], int64), nopython=False, nogil=True)
def smooth(arr_in, func, window):
    """
    Exponentialy weighted moving average specified by a decay ``window`` to provide better adjustments for
    small windows via:
        y[t] = (x[t] + (1-a)*x[t-1] + (1-a)^2*x[t-2] + ... + (1-a)^n*x[t-n]) /
               (1 + (1-a) + (1-a)^2 + ... + (1-a)^n).

    :args
    1. arr_in: (np.ndarray), (float64) A single dimensional numpy array
    2. window: (int64) The decay window, or 'span'

    :return
    (np.ndarray) The EWMA vector, same length / shape as ``arr_in``
    """
    arr_length = arr_in.shape[0]
    filter_singal = np.copy(arr_in)

    for i in range(window-1, arr_length):
        filter_singal[i] = func(x[i-windows_len+1: i+1])[-1]
    return filter_singal
