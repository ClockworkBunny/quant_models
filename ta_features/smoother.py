"""
============================================================
Smoother Function
Author: Zhao Rui, Quant Research, Harveston
===========================================================
"""

import pywt
import numpy as np
from statsmodels.robust import mad
import pandas as pd
def rolling_smoth(x, func, windows_len=300):
    filter_signal = np.copy(x)
    for i in range(windows_len-1, len(x)):
        filter_signal[i] = func(x[i-windows_len+1:i+1])[-1]
    return filter_signal

def waveletSmooth( x, wavelet="db4", level=1, title=None ):
    # calculate the wavelet coefficients  #db4
    coeff = pywt.wavedec( x, wavelet, mode="per" )
    # calculate a threshold
    sigma = mad( coeff[-level] )
    # changing this threshold also changes the behavior,
    # but I have not played with this very much
    uthresh = sigma * np.sqrt( 2*np.log( len( x ) ) )
    coeff[1:] = ( pywt.threshold( i, value=uthresh, mode="soft" ) for i in coeff[1:] )
    # reconstruct the signal using the thresholded coefficients
    y = pywt.waverec( coeff, wavelet, mode="per" )
    return y

wv_filter_har = lambda x: waveletSmooth(x, "db4")


def pd_smooth(df,col='close', smoother = wv_filter_har):
    return pd.Series(rolling_smoth(df.loc[:,col].values, smoother, 5000))