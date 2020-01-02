"""
==============================================
Code for prepare features for CNA BS Model
Author: Zhao Rui, Quant Research, Harveston
==============================================
"""
from ._ta_factors import TAFactor
import pandas as pd
import datetime
import numpy as np


## build your own features


"""
Volume Indicator
Total: 7 dimensions
"""
# On balance Volume
obv = TAFactor("OBV")
# Chaikin A/D Osciallator
adosc = TAFactor("ADOSC",
                kwparams={'fastperiod': [5, 5, 10, 10, 20, 20],
                          'slowperiod': [15, 30, 30,40 40, 60]}
                )

"""
Momentum Indicator
Total: 15 + 3 + 2 = 20
"""
apo = TAFactor("APO", kwparams={
                         'fastperiod': [5, 30, 50],
                         'slowperiod': [10, 60, 100]})
# Ultimate Oscillator
ultosc = TAFactor("ULTOSC", kwparams={
                               'timeperiod1': [5, 10],
                               'timeperiod2': [10, 30],
                               'timeperiod3': [30, 60]})
tplines_mom = [10, 50, 60]]
# Money Flow Index
mfi      = TAFactor("MFI", kwparams={'timeperiod': tplines_mom})
# Minus Directional Indicator
di_minus = TAFactor("MINUS_DI", kwparams={'timeperiod': tplines_mom})
# Plus Directional Indicator
di_plus  = TAFactor("PLUS_DI", kwparams={'timeperiod': tplines_mom})
# COMMODITY Channel Index
cci      = TAFactor("CCI", kwparams={'timeperiod': tplines_mom})
# Relative Strength Index
rsi = TAFactor("RSI", kwparams={ 'timeperiod': tplines_mom})

"""
Stat Indicator
Total: 5 * 2= 10
"""
tplines_stat = [30, 60]
# Pearson's Corrlation Coefficient
correl = TAFactor("CORREL", kwparams={'timeperiod': tplines_stat})
# Linear Regression Slope
linear_slop = TAFactor("LINEARREG_SLOPE", kwparams={'timeperiod': tplines_stat})
# Time Series Forcast
tsf = TAFactor("TSF", kwparams={'timeperiod': tplines_stat})
stddev =  TAFactor("STDDEV", kwparams={'timeperiod': tplines_stat})
zscore =  TAFactor("ZSCORE", kwparams={'timeperiod': tplines_stat})


"""
Volatility Indicator
Total: 2* 4= 8
"""
tplines_vol = [5, 10, 15, 30]
# Normalized Average True Range
natr = TAFactor("NATR", kwparams={'timeperiod': tplines_vol})
# Average True Range
atr =  TAFactor("ATR", kwparams={'timeperiod': tplines_vol})

