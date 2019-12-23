"""
The implementation for the Triple Barrier Method and Meta-Labeling.
The codes are modified from AFML code sinppets.
"""

import numpy as np
import pandas as pd
from util.multiprocess import mp_pandas_obj

def apply_pt_sl_on_ent(df_price, events, pt_sl, molecule):
    """
    From AFML

    This function applies the triple-barrier labeling method. It works on a set of
    datetime index values (molecule). This allows the program to parallelize the processing.

    Mainly it returns a DataFrame of timestamps regarding the time when the first barriers were reached.

    :args
    1. df_price: pd.series
              it should contain the price
    2. events: pd.df
               datetime as index.
               two columns:
                    1. ent: the timestamp of vertical barrier, when the value is np.nan, then no vertical bar
                    2. trgt: the unit width of the horizontal barriers.
    3. pts1: pts1[0]*trgt is the
    4. molecule: a list with the subset of event indcies that will be processed by a single thread.

    :return:
    pd.df
    datetime as index, as the start time
    three cols: 1 ent: the vert bar time
                2 sl:  the time that touch the bottom line (nan means no touch)
                3 pt:  the time that touch the up line (nan means no touch)
    """
    events_ = events.loc[molecule]
    out     = events_[['ent']].copy(deep=True)

    profit_taking_multiple = pt_sl[0]
    stop_loss_multiple     = pt_sl[1]

    # Profit taking active
    if profit_taking_multiple > 0:
        profit_taking = profit_taking_multiple * events_['trgt']
    else:
        profit_taking = pd.Series(index=events.index)  # NaNs

    # Stop loss active
    if stop_loss_multiple > 0:
        stop_loss = -stop_loss_multiple * events_['trgt']
    else:
        stop_loss = pd.Series(index=events.index)  # NaNs

    # Get events
    for loc, vertical_barrier in events_['ent'].fillna(df_price.index[-1]).iteritems():
        closing_prices = df_price[loc: vertical_barrier]  # Path prices for a given trade
        cum_returns = (closing_prices / df_price[loc] - 1) * events_.at[loc, 'side']  # Path returns
        out.loc[loc, 'sl'] = cum_returns[cum_returns < stop_loss[loc]].index.min()  # Earliest stop loss date
        out.loc[loc, 'pt'] = cum_returns[cum_returns > profit_taking[loc]].index.min()  # Earliest profit taking date
    return out



def add_vertical_barrier(df_price, t_events=None, num_days=0, num_hours=0, num_minutes=0, num_seconds=0):
    """
    From AFML, Try to add a Vertical Barrier

    For each index in t_events, it finds the timestamp of the next price bar at or immediately after
    a number of days num_days. This vertical barrier can be passed as an optional argument ent in get_events.

    This function creates a series that has all the timestamps of when the vertical barrier would be reached.

    :args
    1. t_events: DatetimeIndex  Default to be the datetimeindex in the dataframe t
    2. df_price: the price dataframe which has the columns
        datetime as the index
        another column is can be price
    3. Time diff parameters:
        num_days: (int) number of days to add for vertical barrier
        num_hours: (int) number of hours to add for vertical barrier
        num_minutes: (int) number of minutes to add for vertical barrier
        num_seconds: (int) number of seconds to add for vertical barrier'

    :return:
    (series) timestamps of vertical barriers
    """
    if t_events is None:
        t_events = df_price.index
    timedelta = pd.Timedelta(
        '{} days, {} hours, {} minutes, {} seconds'.format(num_days, num_hours, num_minutes, num_seconds))
    # Find index to closest to vertical barrier
    nearest_index = df_price.index.searchsorted(t_events + timedelta)

    # Exclude indexes which are outside the range of close price index
    nearest_index = nearest_index[nearest_index < df_price.shape[0]]

    # Find price index closest to vertical barrier time stamp
    nearest_timestamp = df_price.index[nearest_index]
    filtered_events = t_events[:nearest_index.shape[0]]

    vertical_barriers = pd.Series(data=nearest_timestamp, index=filtered_events)
    return vertical_barriers



def get_events(df_price,
               target,
               t_events=None,
               pt_sl=[1,1],
               min_ret = 0.0,
               num_threads = 1,
               vertical_barrier_times=False,
               side_prediction=None,
               nan_rt_keep=True):
    """
    From AFML

    This function is orchestrator to meta-label the data, in conjunction with the Triple Barrier Method.

    :args:
        1. df_price: the price dataframe which has the columns
        datetime as the index
        another column is can be price
        2. target: pd.series
            values that are used (in conjunction with pt_sl) to determine the width
            of the barrier. In this program this is daily volatility series.
        3. t_events: pd.series
            These are timestamps that will seed every triple barrier. Default to be the datetimeindex in the dataframe t
        4. pt_sl: 2 element array (profit taking level, stop loss level)
            A non-negative float that sets the width of the two barriers. A 0 value means that the respective
            horizontal barrier (profit taking and/or stop loss) will be disabled.
        5. min_ret: folat
            The minimum target return required for running a triple barrier search.
        6. num_threads: int
        7. vertical_barrier_times: pd.series
            A pandas series with the timestamps of the vertical barriers.
            We pass a False when we want to disable vertical barriers.
        8. side_prediction: (series)
            Side of the bet (long/short) as decided by the primary model. Default is 1
        9. nan_rt_keep: boolean value
            If False, drop all bars that the variance is lower than the target bar
            else: use the min_ret as the target return

    :return: (data frame) of events
            -events.index is event's starttime
            -events['ent'] is event's endtime, i.e., the earliest time of up bar touch, low bar touch and the vertical touch
            -events['trgt'] is event's target
            -events['side'] (optional) implies the algo's position side
            -events['pt'] Profit taking multiple
            -events['sl'] Stop loss multiple
    """
    if t_events is None:
        t_events = df_price.index
    # 1) Get target
    target = target.reindex(t_events)
    target.dropna() #in case the t_events doest not match target
    target = target[target > min_ret]  # min_ret

    # 2) Get vertical barrier (max holding period)
    if vertical_barrier_times is False:
        vertical_barrier_times = pd.Series(pd.NaT, index=t_events)

    # 3) Form events object, apply stop loss on vertical barrier
    if side_prediction is None:
        side_ = pd.Series(1.0, index=target.index)
        pt_sl_ = [pt_sl[0], pt_sl[0]]
    else:
        side_ = side_prediction.reindex(target.index) # Subset side_prediction on target index.
        pt_sl_ = pt_sl[:2]

    # Create a new df with [v_barrier, target, side] and drop rows that are NA in target
    events = pd.concat({'ent': vertical_barrier_times, 'trgt': target, 'side': side_}, axis=1)
    events = events.dropna(subset=['side'])
    if nan_rt_keep:
        events = events.fillna(value={'trgt': min_ret})
    events = events.dropna(subset=['trgt'])

    # Apply Triple Barrier It may be very slow
    first_touch_dates = mp_pandas_obj(func=apply_pt_sl_on_ent,
                                      pd_obj=('molecule', events.index),
                                      num_threads=num_threads,
                                      df_price=df_price,
                                      events=events,
                                      pt_sl=pt_sl_)

    events['ent'] = first_touch_dates.dropna(how='all').min(axis=1)  # pd.min ignores nan

    if side_prediction is None:
        events = events.drop('side', axis=1)

    # Add profit taking and stop loss multiples for vertical barrier calculations
    events['pt'] = pt_sl[0]
    events['sl'] = pt_sl[1]

    return events

def barrier_touched(out_df, events):
    """
    From AFML,
    Adjust the getBins function (Snippet 3.7) to return a 0 whenever the vertical barrier is the one touched first.

    Top horizontal barrier: 1
    Bottom horizontal barrier: -1
    Vertical barrier: 0

    : args
        1. out_df: pandas df
          the index is the datetime index
          it has two cols:
            - ret: the acheived return
            - trgt: the target return
        2. events: pandas df
            the index is the datetime index, which is the original events dataframe
    : return
        pd.df, it contain three cols:
            - bin: the generated labels
            - ret
            - target
    """
    store = []
    for date_time, values in out_df.iterrows():
        ret = values['ret']
        target = values['trgt']

        pt_level_reached = ret > target * events.loc[date_time, 'pt']
        sl_level_reached = ret < -target * events.loc[date_time, 'sl']

        if ret > 0.0 and pt_level_reached:
            # Top barrier reached
            store.append(1)
        elif ret < 0.0 and sl_level_reached:
            # Bottom barrier reached
            store.append(-1)
        else:
            # Vertical barrier reached
            store.append(0)

    # Save to 'bin' column and return
    out_df['bin'] = store
    return out_df


def get_bins(triple_barrier_events, df_price):
    """
    From AFML

    Compute event's outcome (including side information, if provided).
    events is a DataFrame where:

    If there is no side col in triple_barrier_events, the bin will be {-1, 0, 1}.
    If there is side col, the bin will be {0,1}, as opposed to whether to take the bet or pass, which is the purely binary prediction.
    In addition, the ML algorithm will be trained to decide is 1, we can use the probability of this secondary prediction
    to derive the size of the bet, where the side (sign) of the position has been set by the primary model.

    : args
    1.  triple_barrier_events: pd.dataframe
        index is datetime type, which is the events' starttime
        have following cols:
            - ent: endtime of the events i.e., the barrier touch time
            - trgt: event's target return
            - side(optional): implies the algo's position side
            - pt: int, the level of profit taking
            - sl: int, the level of loss stoping
            case 1: (side not in the events), assign (-1, 1) to label by price action
            case 2:  side in the events, assign (0, 1) to label by pnl (meta-labeling)
    2   df_price: pd.series close prices

    : return pd.df
        it store the meta-labeled events, dataframe with datetime as the index
        it has three cols:
             - ret: the achieved return
             - target: the targeted return
             - bin: two cases: one is [-1,0,1] and the ohter is [0,1]
    """

    # 1) Align prices with their respective events
    events_ = triple_barrier_events.dropna(subset=['ent'])
    all_dates = events_.index.union(other=events_['ent'].values).drop_duplicates()
    prices = df_price.reindex(all_dates, method='bfill')

    # 2) Create out DataFrame
    out_df = pd.DataFrame(index=events_.index)
    # Need to take the log returns, else your results will be skewed for short positions
    out_df['ret'] = np.log(prices.loc[events_['ent'].values].values) - np.log(prices.loc[events_.index])
    out_df['trgt'] = events_['trgt']

    # Meta labeling: Events that were correct will have pos returns
    if 'side' in events_:
        out_df['ret'] = out_df['ret'] * events_['side']  # meta-labeling

    # Added code: label 0 when vertical barrier reached
    out_df = barrier_touched(out_df, triple_barrier_events)

    # Meta labeling: label incorrect events with a 0
    if 'side' in events_:
        out_df.loc[out_df['ret'] <= 0, 'bin'] = 0

    # Transform the log returns back to normal returns.
    out_df['ret'] = np.exp(out_df['ret']) - 1

    # Add the side to the output. This is useful for when a meta label model must be fit
    tb_cols = triple_barrier_events.columns
    if 'side' in tb_cols:
        out_df['side'] = triple_barrier_events['side']
    return out_df

def drop_labels(events, min_pct=.05):
    """
    From AFML

    This function recursively eliminates rare observations.

    : args:
        - events: pd.dataframe
                  the output from get_bins function
        - min_pct: float number
                   the fraction used to decide if the observation occurs less than that fraction
    : return:
        - data frame of events, dataframe with datetime as the index
        it has three cols:
             - ret: the achieved return
             - target: the targeted return
             - bin: two cases: one is [-1,0,1] and the ohter is [0,1]
    in addition, the program will print the data from the simulated results
    """
    # Apply weights, drop labels with insufficient examples

    while True:
        df0 = events['bin'].value_counts(normalize=True)
        if df0.min() > min_pct or df0.shape[0] < 3:
            break
        print('dropped label: ', df0.argmin(), df0.min())
        events = events[events['bin'] != df0.argmin()]
    return events
