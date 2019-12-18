"""
General python utility functions
"""
import pandas as pd
import pytz as tz
# used by convert_tz func.
TZ_Dict =      {'SG':      tz.timezone('Singapore'),
                'CN':      tz.timezone('Singapore'),
                'US':      tz.timezone('US/Eastern'),
                'UK':      tz.timezone('Europe/London'),
                'Europe':  tz.timezone('Europe/Berlin'),
                'JP':      tz.timezone('Asia/Tokyo')
                }


def get_daily_vol(inputdf, lookback=100, numday=1):
    """
    From AFML books, for each time step, firstly compute the return based on the given numday. Then, apply a span of lookback days to an expoentially weighted moving
    average. It can be used to compute therholds for profit taking and stop loss limites
    :parameters
    inputdf: it is the input dataframe with the columns:
                1. index:   datetime in pd.datetime format
                2. columns: at least close
    lookback: the time interval to compute the ewm volaitilty
    numday:   1

    :return:
    seris of daily volatility value
    """
    closeser = inputdf.close
    df0 = closeser.index.searchsorted(closeser.index - pd.Timedelta(days=numday))
    df0 = df0[df0 > 0]
    df0 = (pd.Series(closeser.index[df0 - 1], index=closeser.index[closeser.shape[0] - df0.shape[0]:]))
    df0 = closeser.loc[df0.index] / closeser.loc[df0.values].values - 1  # daily returns
    df0 = df0.ewm(span=lookback).std()
    outputdf  = df0.to_frame(name='vol')
    outputdf.dropna(inplace=True)
    return outputdf

def sample_df(inputdf, freq='1D'):
    """
    the function that sample the dataframe based on the input sampling
    frequency. S, T, H, D, M denotes second, minute, hour, day and month

    :param
    inputdf: it is the input dataframe with the columns:
                1. index:   datetime in pd.datetime format
                2. columns: high, open, low, close, volume(potential)
    freq: the sampling frequency, which can be '1D', '5m' and so on

    :return
    the dataframe that is resampled based on freq
    """
    dfoutput           = pd.DataFrame()
    dfoutput['open']   = inputdf.open.resample(freq).first()
    dfoutput['close']  = inputdf.close.resample(freq).last()
    dfoutput['low']    = inputdf.low.resample(freq).min()
    dfoutput['high']   = inputdf.high.resample(freq).max()
    if 'volume' in inputdf.columns:
        dfoutput['volume'] = inputdf.volume.resample(freq).sum()
    dfoutput.sort_index(inplace=True)
    dfoutput.dropna(inplace=True)
    return dfoutput

def convert_tz(inputdf, src='SG', tar='US'):
    """
    Convert the timezone of datatime index.
    Supported regions: SG, US, CN, UK, Europe, JP


    :param
    inputdf: it is the input dataframe with the columns:
                1. index:   datetime in pd.datetime format
    src: the abbreviation of source time zone
    tar: the abbreviation of target time zone

    :return
    the dataframe with the new time zone
    """
    output_df = inputdf.copy()
    output_df.index = output_df.index.tz_localize(TZ_Dict[src])  \
                               .tz_convert(TZ_Dict[tar])  \
                               .tz_localize(None)
    return output_df

def filter_df_time(inputdf,
                   time_range=[('09:30', '15:59')]):
    """
    Filter the inputdf based on time and hours.

    :param
    inputdf: it is the input dataframe with the columns:
                1. index:   datetime in pd.datetime format
    time_range: a list of tuple (st, et)
                each time is in %h:%m formats
                the points on st and et will be sampled

    :return
    subdataframe
    """
    outputdf = inputdf.copy()
    all_df = []
    for sub_range in time_range:
        st, et = sub_range[0], sub_range[1]
        subdf = outputdf.between_time(st, et)
        all_df.append(subdf)
    outputdf = pd.concat(all_df)
    outputdf.sort_index(inplace=True)
    return outputdf