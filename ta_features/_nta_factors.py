"""
Inhouse Wrappers for Customed Indicators

We compute the indicators that is in a normalized range
"""
import pandas as pd
import numpy as np
import talib
from ._base_factors import Factor

class NTAFactor(Factor):
    KNOWN_FACTORS = ['NAPO', 'NBOLL', 'NAPOEMA_factor', 'NADOSC_Factor', 'NAD_Factor']

    def __init__(self, name, map_dict={}, params=[], kwparams={}, outname=[]):
        if name in self.KNOWN_FACTORS:
            CALLER_MAP = {'NAPO':           [self.NAPO_factor, ['NAPO']],
                          'NBOLL':          [self.NBOLL_Factor, ['NBOLL']],
                          'NAPOEMA_factor': [self.NAPOEMA_factor, ['NAPOEMA_factor']],
                          'NADOSC_Factor':  [self.NADOSC_Factor, ['NADOSC_Factor']],
                          'NAD_Factor':     [self.NAD_Factor, ['NAD_Factor']],
                          }
            caller = CALLER_MAP[name][0]
            if len(outname) > 0:
                super(NTAFactor, self).__init__(
                    name, caller, params, kwparams, outname)
            else:
                super(NTAFactor, self).__init__(
                    name, caller, params, kwparams, CALLER_MAP[name][1])

            self.map_dict = {'close': 'close',
                             'open': 'open',
                             'high': 'high',
                             'low': 'low',
                             'volume': 'volume',
                             'default': 'open'}

            for key in map_dict:
                self.map_dict[key] = map_dict[key]
        else:
            raise IndexError('Unknown TA.')


    def NAPO_factor(self, df, fastperiod=12, slowperiod=26, matype=0):
        """
        the custom function that compute normalized apo
        the equation is (fast ma - slow ma)/slowma
        """
        numerator   =  talib.APO(df.loc[:, self.map_dict['default']].values,
                                fastperiod, slowperiod, matype)
        denominator =  talib.MA(df.loc[:, self.map_dict['default']].values,
                                slowperiod, matype)
        return numerator/denominator

    def NAPOEMA_factor(self, df, fastperiod=12, slowperiod=26, matype=0):
        """
        the custom function that compute normalized apo
        the equation is (fast ma - slow ma)/slowma
        """
        numerator   =  talib.APO(df.loc[:, self.map_dict['default']].values,
                                fastperiod, slowperiod, matype)
        denominator =  talib.EMA(df.loc[:, self.map_dict['default']].values,
                                slowperiod, matype)
        return numerator/denominator

    def NBOLL_Factor(self, df, timeperiod):
        """
        the custom function that compute normalized bollinger band features
        the equation is 2*(price-middle)/(up-bottom)
        """
        upperband, middleband, lowerband = talib.BBANDS(df.loc[:, self.map_dict['default']].values,
                                                        timeperiod=timeperiod,
                                                        nbdevup=2,
                                                        nbdevdn=2,
                                                        matype=0)
        return 2*(df.loc[:, self.map_dict['default']].values - middleband) / (upperband - lowerband)



    def NAD_Factor(self, df, normperiod=100):
        """
        the custom function that compute normalized  AD
        the equation is (ind - recentlow) / (recenthigh - recentlow)
        range 0-1
        """
        real  = talib.AD(df.loc[:, self.map_dict['high']].values,
                         df.loc[:, self.map_dict['low']].values,
                         df.loc[:, self.map_dict['close']].values,
                         df.loc[:, self.map_dict['volume']].values)
        min_val, max_val = talib.MINMAX(real, timeperiod=normperiod)

        final_fea = (real - min_val) / (max_val - min_val)
        return final_fea

    def NADOSC_Factor(self, df, fastperiod=12, slowperiod=24, normperiod=100):
        """
        the custom function that compute normalized ADOSC
        range 0-1
        """
        real  = talib.ADOSC(df.loc[:, self.map_dict['high']].values,
                           df.loc[:, self.map_dict['low']].values,
                           df.loc[:, self.map_dict['close']].values,
                           df.loc[:, self.map_dict['volume']].values,
                           fastperiod=fastperiod,
                           slowperiod=slowperiod)
        min_val, max_val = talib.MINMAX(real, timeperiod=normperiod)

        final_fea = (real - min_val) / (max_val - min_val)
        return final_fea

if __name__ == '__main__':
    #design factor
    stoch = NTAFactor('NAPO', kwparams={'fast_period': [
                     9, 9, 9, 5, 5, 5], 'slow_period': [6, 3, 2, 4, 3, 2]})
