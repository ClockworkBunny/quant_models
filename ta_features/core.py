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
Momentum Indicator
Total: 6*3 + 1= 19
"""
TPLINES_MOM_L = [40, 50, 60]
TPLINES_MOM_S = [5, 15, 25]
# Money Flow Index
mfi      = TAFactor("MFI", kwparams={'timeperiod': TPLINES_MOM_L})
# Minus Directional Indicator
di_minus = TAFactor("MINUS_DI", kwparams={'timeperiod': TPLINES_MOM_S})
# Plus Directional Indicator
di_plus  = TAFactor("PLUS_DI", kwparams={'timeperiod': TPLINES_MOM_L})
# COMMODITY Channel Index
cmo      = TAFactor("CMO", kwparams={'timeperiod': TPLINES_MOM_S})
# Relative Strength Index
rsi = TAFactor("RSI", kwparams={'timeperiod': TPLINES_MOM_L})

# Williams' %R
willr =  TAFactor("WILLR", kwparams={'timeperiod': TPLINES_MOM_S})

# Balance of Power
bop = TAFactor("BOP")


"""
Stat Indicator
Total: 5 * 4= 20
"""
TPLINE_STAT = [5, 15, 30, 60]
# Pearson's Corrlation Coefficient
correl = TAFactor("CORREL", kwparams={'timeperiod': TPLINE_STAT})
# Linear Regression Slope
linear_slop = TAFactor("LINEARREG_SLOPE", kwparams={'timeperiod': TPLINE_STAT})
stddev =  TAFactor("STDDEV", kwparams={'timeperiod': TPLINE_STAT})
zscore =  TAFactor("ZSCORE", kwparams={'timeperiod': TPLINE_STAT})

"""
Volatility Indicator
Total: 6
"""
TPLINE_VOL = [5, 15, 25, 35, 50, 60]
# Normalized Average True Range
natr = TAFactor("NATR", kwparams={'timeperiod': TPLINE_VOL})


DEFAULT_COLS_paras = [mfi, di_minus,di_plus, rsi, willr, cmo, correl, linear_slop, stddev, zscore,natr]
DEFAULT_COLS       = [bop]


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

