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

    def transform(self, df):
        """
        Constructor

        # args
            threshold : the sampling threshold
            dictcol : dict that map col names to defined col names (datetime, price, volume)
        """
        if self.dictcol != None:
            df.rename(columns=self.dictcol, inplace=True)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime')
            df.drop_duplicates()
        else:
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime')
            df.drop_duplicates()            
        self._assert_csv(df)
        ref_idx = self._extract_bars(df)
        return self._create_bars(df, ref_idx)

    @abstractmethod
    def _extract_bars(self, data):
        """
        This method is required by all the bar types and is used to create the desired bars.
        :param data: (DataFrame) Contains 3 columns - date_time, price, and volume.
        :return: (List) of bars built using the current batch.
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
        '''
        fn: get ohlc from custom bars
    
        # args
            df : reference pandas dataframe with all prices and volume
            sub : custom tick pandas series (index is the datetime, the column is the price)
        # returns
            tick_df : dataframe with ohlcv values, which is the ending time index
        '''
        ohlcv = []
        for i in range(sub.index.shape[0]-1):
            start,end = sub.index[i], sub.index[i+1]
            tmp_df = df.loc[start:end]
            max_px, min_px = tmp_df.price.max(), tmp_df.price.min()
            vol          = tmp_df.volume.sum()
            o, h, l, c, vol = sub.iloc[i], max_px, min_px, sub.iloc[i+1], vol
            ohlcv.append((end,o,h,l,c, vol))
        cols = ['datetime','open','high','low','close', 'volume']
        return (pd.DataFrame(ohlcv,columns=cols))
   