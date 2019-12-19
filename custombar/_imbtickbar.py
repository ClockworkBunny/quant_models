"""
A base class for the various bar types. Includes the logic shared between classes, to minimise the amount of
duplicated code.
"""


import pandas as pd
import numpy as np
from ._base_bars import _BaseBars
from util import ewma

class Imbalance_Bar(_BaseBars):
    """
    Abstract base class which contains the structure which is shared between the various standard and information
    driven bars. There are some methods contained in here that would only be applicable to information bars but
    they are included here so as to avoid a complicated nested class structure.
    """

    def __init__(self, threshold=None, dictcol=None, mode='tick', num_prev_bars=3, exp_num_ticks_init=5000):
        """
        Constructor

        # args
            threshold : the sampling threshold
            dictcol : dict that map col names to defined col names (datetime, price, volume)
            mode: it can be tick, or volume or dollar
            num_prev_bars: how many previous bars are checked for expectation
            exp_num_ticks_init: the inital guess of expectation of sampled information
        """
        # Base properties
        _BaseBars.__init__(self, threshold, dictcol)
        # Information bar properties
        self.num_prev_bars = num_prev_bars
        self.exp_num_ticks_init = exp_num_ticks_init
        # Expected number of ticks extracted from prev bars
        self.exp_num_ticks = self.exp_num_ticks_init
        self.num_ticks_bar = []  # List of number of ticks from previous bars

        self.expected_imbalance = np.nan
        self.imbalance_array = []
        self.metric  = mode

    def _extract_bars(self, inputdf):
        """
        method that extract the index of rows for sampling
        # args
            inputdf : the dataframe that has three columns price, volume and datetime
        # return:
            the dataframe only containing the boundary datetime for each sample interval
        """
        df_used = inputdf.copy()
        df_used = df_used[['price', 'volume']]
        cum_theta      = 0
        idx     = []
        cum_ticks = 0
        for i in range(df_used.shape[0]):
            dfrow  = df_used.iloc[i,:]
            price  = dfrow.price
            volume = dfrow.volume
            signed_tick = self._apply_tick_rule(price)
            imbalance   = self._get_imbalance(price, signed_tick, volume)
            self.imbalance_array.append(imbalance)
            cum_theta += imbalance
            cum_ticks += 1
            if np.isnan(self.expected_imbalance):
                self.expected_imbalance = self._get_expected_imbalance(self.exp_num_ticks,
                                                                       self.imbalance_array)
            if np.abs(cum_theta) > self.exp_num_ticks * np.abs(self.expected_imbalance):
                self.num_ticks_bar.append(cum_ticks)
                # Expected number of ticks based on formed bars
                self.exp_num_ticks = ewma(np.array(
                    self.num_ticks_bar[-self.num_prev_bars:], dtype=float), self.num_prev_bars)[-1]

                self.expected_imbalance = self._get_expected_imbalance(
                    self.exp_num_ticks * self.num_prev_bars, self.imbalance_array)
                idx.append(i)
                cum_ticks, cum_theta = 0, 0
                self.prev_tick['price'] = price
                continue
            self.prev_tick['price'] = price
        return inputdf.iloc[idx,:].index.drop_duplicates()

    def _get_expected_imbalance(self, window, imbalance_array):
        """
        Calculate the expected imbalance: 2P[b_t=1]-1, using a EWMA, pg 29
        :param window: EWMA window for calculation
        :param imbalance_array: (numpy array) of the tick imbalances
        :return: expected_imbalance: 2P[b_t=1]-1, approximated using a EWMA
        """
        if len(imbalance_array) < self.exp_num_ticks_init:
            # Waiting for array to fill for ewma
            ewma_window = np.nan
        else:
            # ewma window can be either the window specified in a function call
            # or it is len of imbalance_array if window > len(imbalance_array)
            ewma_window = int(min(len(imbalance_array), window))

        if np.isnan(ewma_window):
            # return nan, wait until len(imbalance_array) >= self.exp_num_ticks_init
            expected_imbalance = np.nan
        else:
            expected_imbalance = ewma(
                np.array(imbalance_array[-ewma_window:], dtype=float), window=ewma_window)[-1]

        return expected_imbalance

    def _get_imbalance(self, price, signed_tick, volume):
        """
        Get the imbalance at a point in time, denoted as Theta_t in the book, pg 29.

        :param price: Price at t
        :param signed_tick: signed tick, using the tick rule
        :param volume: Volume traded at t
        :return: Imbalance at time t
        """
        if self.metric == 'tick':
            imbalance = signed_tick
        if self.metric == 'dollar':
            imbalance = signed_tick * volume * price
        if self.metric == 'volume':
            imbalance = signed_tick * volume
        else:
            imbalance = signed_tick
        return imbalance