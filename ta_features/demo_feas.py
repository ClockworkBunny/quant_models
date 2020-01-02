"""
============================================================
TA Indicator Extraction
Author: Zhao Rui, Quant Research, Harveston
===========================================================
"""
from ._ta_factors import TAFactor
import pandas as pd
import datetime
import numpy as np
"""
Single Factor Create
Basically Two Class:
1 without parameters:
bop = fg.TAFactor("BOP")
2 with parameters:
cci = fg.TAFactor("CCI", kwparams={'timeperiod': [5, 10, 30, 50]})
ultosc = fg.TAFactor("ULTOSC", kwparams={
                               'timeperiod1': [30, 50],
                               'timeperiod2': [60, 100],
                               'timeperiod3': [120, 200]})
"""
tplines = [5, 30, 50, 70]

"""
Volume Indicator
"""
# On balance Volume
obv = TAFactor("OBV")
# Chaikin A/D Osciallator
adosc = TAFactor("ADOSC", kwparams={
    'fastperiod': [5, 30],
    'slowperiod': [20, 60]})
######Volume Indicator End######

"""
Monmentum Indicator
"""
# Absolute Price Oscillator
apo = TAFactor("APO", kwparams={
                         'fastperiod': [5, 30, 50],
                         'slowperiod': [10, 60, 100]})
# Ultimate Oscillator
ultosc = TAFactor("ULTOSC", kwparams={
                               'timeperiod1': [10, 30],
                               'timeperiod2': [30, 60],
                               'timeperiod3': [60, 100]})
# Aroon
aroon    = TAFactor("AROON", kwparams={'timeperiod': tplines})
# Chande Momentum Oscillator
cmo      = TAFactor("CMO", kwparams={'timeperiod': tplines})
# Directional Movement Index
dx       = TAFactor("DX", kwparams={'timeperiod': tplines})
# Money Flow Index
mfi      = TAFactor("MFI", kwparams={'timeperiod': tplines})
# Minus Directional Indicator
di_minus = TAFactor("MINUS_DI", kwparams={
                       'timeperiod': tplines})
# Plus Directional Indicator
di_plus  = TAFactor("PLUS_DI", kwparams={
                      'timeperiod': tplines})
# Rate of Change
roc      = TAFactor("ROC", kwparams={'timeperiod': tplines})
# 1 day rate-of-change of a triple smooth EMA
trix     = TAFactor("TRIX", kwparams={'timeperiod': tplines})
# COMMODITY Channel Index
cci      = TAFactor("CCI", kwparams={
                                  'timeperiod': tplines})
# Relative Strength Index
rsi = TAFactor("RSI", kwparams={
                                   'timeperiod': tplines})
# Average Directional Movement Index Rating
adxr = TAFactor("ADXR", kwparams={
                                    'timeperiod': tplines})

# Williams' %R
willr =  TAFactor("WILLR", kwparams={
                          'timeperiod': tplines})
# Momentum
mom = TAFactor("MOM", kwparams={
                          'timeperiod': tplines})
# Balance of Power
bop = TAFactor("BOP")
######Momentum Indicator End######


"""
Stat Indicator
"""
# Pearson's Corrlation Coefficient
correl = TAFactor("CORREL", kwparams={
                                     'timeperiod': tplines})
# Linear Regression Slope
linear_slop = TAFactor("LINEARREG_SLOPE", kwparams={
                                     'timeperiod': tplines})
# Time Series Forcast
tsf = TAFactor("TSF", kwparams={
                                    'timeperiod': tplines})

linearreg = TAFactor("LINEARREG", kwparams={
                          'timeperiod': tplines})
linear_intercept = TAFactor("LINEARREG_INTERCEPT", kwparams={
                          'timeperiod': tplines})

stddev =  TAFactor("STDDEV", kwparams={
                          'timeperiod': tplines})
zscore =  TAFactor("ZSCORE", kwparams={
                          'timeperiod': tplines})
######Stat Indicator End######

"""
Volatility Indicator
"""
# Normalized Average True Range
natr = TAFactor("NATR", kwparams={
                                   'timeperiod': tplines})
# Average True Range
atr =  TAFactor("ATR", kwparams={
                          'timeperiod': tplines})
# True Range
trange = TAFactor("TRANGE")
######Vol Indicator End######
"""
Overlap Studies
"""
# double exponential moving average
dema = TAFactor("DEMA", kwparams={
                          'timeperiod': tplines})

# exponential moving average
ema = TAFactor("EMA", kwparams={
                          'timeperiod': tplines})
# Hilbert Transform - Instantaneous Trendline
ht_trendline = TAFactor("HT_TRENDLINE")
# Kaufman Adpative Moving Average
kama = TAFactor("KAMA", kwparams={
                          'timeperiod': tplines})
# Simply Moving Average
sma = TAFactor("SMA", kwparams={
                          'timeperiod': tplines})
# Triple Exponential Moving Average (T3)
t3 = TAFactor("T3", kwparams={
                          'timeperiod': tplines})
# Weighted Moving Average
wma = TAFactor("WMA", kwparams={
                          'timeperiod': tplines})
######Overlap Indicator End######





DEFAULT_COLS_paras = [cci, natr, tsf, roc, cmo, rsi, correl, adxr, trix,
                      linear_slop, ultosc, zscore, dema, ema, kama, sma,
                      t3, wma, mom, linearreg, linear_intercept, willr, atr]
DEFAULT_COLS       = [trange, obv, bop, ht_trendline]
DEFAULT_COLS_v1    = [trange, bop, ht_trendline]

def extract_tafea(df, col_paras=DEFAULT_COLS_paras, cols=DEFAULT_COLS):
    """
    extract ta features, return the dataframe with features columns
    inputs:
     - df: should contain symbol, date, close, high, open, low and volume
           sort by date
     - col_paras: features names that need hyper-parameters
     - col: features names that do not need hyper-parameters
     return:
     - df: that will contain feature columns
    """
    features = col_paras[0].run(df)
    for idx in range(1, len(col_paras)):
        features.extend(col_paras[idx].run(df))
    for col in cols:
        features.append(col(df))
    return pd.concat(features, axis=1)

def extract_tafea_withp(df, col_paras=DEFAULT_COLS_paras, cols=DEFAULT_COLS_v1):
    """
    extract ta features, return the dataframe with features columns
    it will not inclue volume info
    inputs:
     - df: should contain symbol, date, close, high, open, low and volume
           sort by date
     - col_paras: features names that need hyper-parameters
     - col: features names that do not need hyper-parameters
     return:
     - df: that will contain feature columns
    """
    features = col_paras[0].run(df)
    for idx in range(1, len(col_paras)):
        features.extend(col_paras[idx].run(df))
    for col in cols:
        features.append(col(df))
    return pd.concat(features, axis=1)

if __name__ == '__main__':
    symbol = ['1'] * 50 + ['2']*50
    date1 = '2017-10-13'
    start = datetime.datetime.strptime(date1, '%Y-%m-%d')
    step = datetime.timedelta(days=1)
    dates = []
    for i in range(50):
        dates.append(start.date())
    all_dates = dates + dates
    closes = np.random.rand(100,)
    opens = np.random.rand(100,)
    lows = np.random.rand(100,)
    highs = np.random.rand(100,)
    volumes = np.random.rand(100,)
    dict_data = {'symbol': symbol, 'date': all_dates, 'close': closes, 
                 'open': opens, 'low': lows, 'high': highs, 'volume': volumes}
    df = pd.DataFrame.from_dict(dict_data)
    # test feat
    df.sort_values(by=['symbol', 'date'], inplace=True)
    df.dropna(inplace=True)
    df_fea = df.groupby('symbol').apply(extract_tafea)
    print(df_fea.head(2))

