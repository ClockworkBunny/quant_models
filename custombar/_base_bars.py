"""
A base class for the various bar types.
"""

from abc import ABC, abstractmethod

import pandas as pd
import numpy as np


class _BaseBars(ABC):
    """
    Abstract base class which contains the structure which is shared between the various standard and information
    driven bars. There are some methods contained in here that would only be applicable to information bars but
    they are included here so as to avoid a complicated nested class structure.
    """

    def __init__(self, threshold=None, dictcol=None):
        """
        Constructor

        # args
            threshold : the sampling threshold
            dictcol : dict that map col names to defined col names (datetime, price, volume)
        """
        # Base properties
        self.dictcol   = dictcol
        self.threshold = threshold
        # these two vars will be used for imbalance bar
        self.prev_tick = {}
        self.prev_tick_rule = 0

    def transform(self, df):
        """
        Constructor

        # args
            threshold : the sampling threshold
            dictcol : dict that map col names to defined col names (datetime, price, volume)
        """
        if self.dictcol != None:
            df.rename(columns=self.dictcol, inplace=True)
            df.drop_duplicates()
        else:
            df.drop_duplicates()
        df = df[['price', 'volume']]
        self._assert_csv(df)
        df.sort_index(inplace=True)
        ref_idx = self._extract_bars(df)
        return self._create_bars(df, ref_idx)

    @abstractmethod
    def _extract_bars(self, data):
        """
        This method is required by all the bar types and is used to create the desired bars.
        # args
            data : the input data which has date as the index, which has two columns: price and volume
        # returns
            data : dataframe with ohlcv values, which is the ending time index
        """

    @staticmethod
    def _assert_csv(df):
        """
        Tests that the csv file read has the format: date_time, price, and volume.
        If not then the user needs to create such a file. This format is in place to remove any unwanted overhead.

        :param test_batch: (DataFrame) the first row of the dataset.
        """
        assert df.shape[1] == 2, 'Must have only 2 columns in csv: price, & volume.'
        assert isinstance(df.iloc[0, :]['price'], float), 'price column in csv not float.'
        assert not isinstance(df.iloc[0, :]['volume'], str), 'volume column in csv not int or float.'

        try:
            pd.to_datetime(df.index[0])
        except ValueError:
            print('the index, not a date time format:',
                  df.index[0].iloc[0, 0])


    def _create_bars(self, df, sub):
        """
        fn: get ohlc from custom bars

        # args
            df : reference pandas dataframe with all prices and volume
            sub : datetime index
        # returns
            tick_df : dataframe with ohlcv values, which is the ending time index
        """
        ohlcv = []
        for i in range(sub.shape[0]-1):
            start,end         = sub[i], sub[i+1]
            tmp_df            = df.loc[start:end]
            max_px, min_px    = tmp_df.price.max(), tmp_df.price.min()
            open_px, close_px = tmp_df.iloc[0].price, tmp_df.iloc[-1].price
            vol               = tmp_df.volume.sum()
            o, h, l, c, vol   = open_px, max_px, min_px, close_px, vol
            ohlcv.append((start,o,h,l,c, vol))
        cols  = ['datetime','open','high','low','close', 'volume']
        outdf = pd.DataFrame(ohlcv,columns=cols)
        outdf.set_index('datetime', inplace=True)
        outdf.sort_index(inplace=True)
        return outdf

    def _apply_tick_rule(self, price):
        """
        Applies the tick rule as defined on page 29.

        :param price: Price at time t
        :return: The signed tick
        """
        if self.prev_tick:
            tick_diff = price - self.prev_tick['price']
        else:
            tick_diff = 0
        signed_tick = 0
        if tick_diff != 0:
            signed_tick = np.sign(tick_diff)
            self.prev_tick_rule = signed_tick
        else:
            signed_tick = self.prev_tick_rule

        return signed_tick