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
    frequency

    :param
    inputdf: it is the input dataframe with the columns:
                1. index:   datetime in pd.datetime format
                2. columns: high, open, low, close, volume(potential)
    freq: the sampling frequency, which can be '1D', '5m' and so on

    :return
    the dataframe that is resampled based on freq
    """
    inputdf.set_index('datetime', inplace=True)
    sampled_df           = pd.DataFrame()
    sampled_df['open']   = sampled_df.open.resmaple(freq).first()
    sampled_df['close']  = sampled_df.close.resmaple(freq).last()
    sampled_df['low']    = sampled_df.low.resmaple(freq).min()
    sampled_df['high']   = sampled_df.high.resmaple(freq).max()
    if 'volume' in sampled_df.columns:
        sampled_df['volume'] = sampled_df.volume.resmaple(freq).sum()
    sampled_df.reset_index(level=0, inplace=True)
    sampled_df.sort_values(by=['datetime'], inplace=True)
    sampled_df.dropna(inplace=True)
    return sampled_df

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

def filter_df_time(inputdf, )