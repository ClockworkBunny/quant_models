"""
A base class for the various bar types. Includes the logic shared between classes, to minimise the amount of
duplicated code.
"""


import pandas as pd
import numpy as np
from ._base_bars import _BaseBars
from util import ewma

class Imbalance_TickBar(_BaseBars):
    """
    Abstract base class which contains the structure which is shared between the various standard and information
    driven bars. There are some methods contained in here that would only be applicable to information bars but
    they are included here so as to avoid a complicated nested class structure.
    """

    def __init__(self, threshold=None, dictcol=None, num_prev_bars=3, exp_num_ticks_init=50000):
        """
        Constructor

        :param file_path: (String) Path to the csv file containing raw tick data in the format[date_time, price, volume]
        :param metric: (String) type of imbalance bar to create. Example: dollar_imbalance.
        :param batch_size: (Int) Number of rows to read in from the csv, per batch.
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



    def _extract_bars(self, inputdf):
        """
        This method is required by all the bar types and is used to create the desired bars.
        :param data: (DataFrame) Contains 3 columns - date_time, price, and volume.
        :return: (List) of bars built using the current batch.
        """
        t_price = inputdf['price']
        cum_theta      = 0
        idx     = []
        cum_ticks = 0
        for i, price in enumerate(t_price):
            imbalance = self._apply_tick_rule(price)
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


        return t_price.iloc[idx].drop_duplicates()

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