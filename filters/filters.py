"""
Filters are used to filter events based on some kind of trigger.
Events are used to measure the return from the events.
"""
import numpy as np
import pandas as pd

def cusum_filter(raw_time_series, threshold, time_stamps=True):
    """
    This method is required by all the bar types and is used to create the desired bars.
    :param
    1. raw_time_series: (series) of close prices (or other time series, e.g. volatility).
    2. threshold:       (float or pd.Series) when the abs(change) is larger than the threshold, the function captures
    it as an event, can be dynamic if threshold is pd.Series
    3. time_stamps:   DateTimeIndex if true a list than false

    :return: (datetime index vector) vector of datetimes when the events occurred. This is used later to sample.
    """
    t_events = []
    s_pos = 0
    s_neg = 0

    # log returns
    raw_time_series = pd.DataFrame(raw_time_series)  # Convert to DataFrame
    raw_time_series.columns = ['price']
    raw_time_series['log_ret'] = raw_time_series.price.apply(np.log).diff()
    if isinstance(threshold, (float, int)):
        raw_time_series['threshold'] = threshold
    elif isinstance(threshold, pd.Series):
        raw_time_series.loc[threshold.index, 'threshold'] = threshold
    else:
        raise ValueError('threshold is neither float nor pd.Series!')

    raw_time_series = raw_time_series.iloc[1:]  # Drop first na values
    # Get event time stamps for the entire series
    # each tup will be row data in pandas series
    for tup in raw_time_series.itertuples():
        thresh = tup.threshold
        pos   = float(s_pos + tup.log_ret)
        neg   = float(s_neg + tup.log_ret)
        s_pos = max(0.0, pos)
        s_neg = min(0.0, neg)
        if s_neg < -thresh:
            s_neg = 0
            t_events.append(tup.Index)
        elif s_pos > thresh:
            s_pos = 0
            t_events.append(tup.Index)
    # Return DatetimeIndex or list
    if time_stamps:
        event_timestamps = pd.DatetimeIndex(t_events)
        return event_timestamps
    return t_events


def z_score_filter(pd_series, mean_window, std_window, z_score=3, time_stamps=True):
    """
    Z-score filter
    :param
    1. pd_series: (series) of close prices (or other time series, e.g. volatility).
    2. mean_window:  rolling mean window, int
    3. std_window:   rolling std window, int
    4. z_score:      number of standard deviations to trigger the event, float
    5. time_stamps:  DateTimeIndex if true a list than false

    :return: (datetime index vector) vector of datetimes when the events occurred. This is used later to sample.
    """
    t_events = pd_series[pd_series >= pd_series.rolling(window=mean_window).mean() +
                               z_score * pd_series.rolling(window=std_window).std()].index
    if time_stamps:
        event_timestamps = pd.DatetimeIndex(t_events)
        return event_timestamps
    return t_events
