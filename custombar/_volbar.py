"""
A base class for the various bar types. Includes the logic shared between classes, to minimise the amount of
duplicated code.
"""


import pandas as pd
import numpy as np
from ._base_bars import _BaseBars

class VolBar(_BaseBars):
    """
    Abstract base class which contains the structure which is shared between the various standard and information
    driven bars. There are some methods contained in here that would only be applicable to information bars but
    they are included here so as to avoid a complicated nested class structure.
    """

    def __init__(self, threshold=None, dictcol=None):
        """
        Constructor

        :param file_path: (String) Path to the csv file containing raw tick data in the format[date_time, price, volume]
        :param metric: (String) type of imbalance bar to create. Example: dollar_imbalance.
        :param batch_size: (Int) Number of rows to read in from the csv, per batch.
        """
        # Base properties
        _BaseBars.__init__(self, threshold, dictcol)



    def _extract_bars(self, inputdf):
        """
        This method is required by all the bar types and is used to create the desired bars.
        :param data: (DataFrame) Contains 3 columns - date_time, price, and volume.
        :return: return datetimeIndex
        """
        t_vol = inputdf['volume']
        ts      = 0
        idx     = []
        for i, x in enumerate(t_vol):
            ts += x
            if ts >= self.threshold:
                idx.append(i)
                ts = 0
                continue
        return inputdf.iloc[idx,:].index.drop_duplicates()
