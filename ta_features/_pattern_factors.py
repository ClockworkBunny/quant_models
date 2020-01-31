"""
Inhouse Wrappers for Pattern Factors

The idea is that given these pattern indicators,
we will count the number of buy sign, sell sign given the lookback period
"""
import pandas as pd
import numpy as np
import talib
from ._base_factors import Factor

USED_PATTERN = ['CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3LINESTRIKE', 'CDL3OUTSIDE', 'CDL3STARSINSOUTH',
                'CDL3WHITESOLDIERS', 'CDLABANDONEDBABY', 'CDLADVANCEBLOCK', 'CDLBELTHOLD', 'CDLBREAKAWAY',
                'CDLCLOSINGMARUBOZU', 'CDLCONCEALBABYSWALL', 'CDLCOUNTERATTACK', 'CDLDARKCLOUDCOVER',
                'CDLDOJI', 'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 'CDLENGULFING', 'CDLEVENINGDOJISTAR', 'CDLEVENINGSTAR',
                'CDLGAPSIDESIDEWHITE', 'CDLGRAVESTONEDOJI', 'CDLHAMMER', 'CDLHANGINGMAN', 'CDLHARAMI', 'CDLHARAMICROSS',
                'CDLHIGHWAVE', 'CDLHIKKAKE', 'CDLHIKKAKEMOD', 'CDLHOMINGPIGEON', 'CDLIDENTICAL3CROWS', 'CDLINNECK',
                'CDLINVERTEDHAMMER', 'CDLKICKING','CDLKICKINGBYLENGTH', 'CDLLADDERBOTTOM', 'CDLLONGLEGGEDDOJI',
                'CDLLONGLINE', 'CDLMARUBOZU', 'CDLMATCHINGLOW', 'CDLMATHOLD', 'CDLMORNINGDOJISTAR', 'CDLMORNINGSTAR', 'CDLONNECK',
                'CDLPIERCING', 'CDLRICKSHAWMAN', 'CDLRISEFALL3METHODS', 'CDLSEPARATINGLINES', 'CDLSHOOTINGSTAR', 'CDLSHORTLINE',
                'CDLSPINNINGTOP', 'CDLSTALLEDPATTERN', 'CDLSTICKSANDWICH', 'CDLTAKURI', 'CDLTASUKIGAP', 'CDLTHRUSTING',
                'CDLTRISTAR', 'CDLUNIQUE3RIVER', 'CDLUPSIDEGAP2CROWS', 'CDLXSIDEGAP3METHODS']

class PatternFactor(Factor):
    KNOWN_FACTORS = ['Pattern_num']

    def __init__(self, name, map_dict={}, params=[], kwparams={}, outname=[]):
        if name in self.KNOWN_FACTORS:
            CALLER_MAP = {'Pattern_num': [self.Patternnum, ['Pattern_num']]
                          }
            caller = CALLER_MAP[name][0]
            if len(outname) > 0:
                super(PatternFactor, self).__init__(
                    name, caller, params, kwparams, outname)
            else:
                super(PatternFactor, self).__init__(
                    name, caller, params, kwparams, CALLER_MAP[name][1])

            self.map_dict = {'close': 'close',
                             'open': 'open',
                             'high': 'high',
                             'low': 'low',
                             'volume': 'volume',
                             'default': 'close'}

            for key in map_dict:
                self.map_dict[key] = map_dict[key]
        else:
            raise IndexError('Unknown TA.')


    def Patternnum(self, df, timeperiod=0,patterns=USED_PATTERN):
        """
        the custom function that compute normalized apo
        the equation is (fast ma - slow ma)/slowma
        """
        pattern_list = []
        for  upattern in patterns:
            pattern_ind = getattr(talib, upattern)(df.loc[:, self.map_dict['open']].values,
                                     df.loc[:, self.map_dict['high']].values,
                                     df.loc[:, self.map_dict['low']].values,
                                     df.loc[:, self.map_dict['close']].values
                                   )
            pattern_list.append(pattern_ind)
        final_pattern = np.add.reduce(pattern_list)
        final_pattern = final_pattern/100.0
        if timeperiod > 0:
            final_pattern = talib.EMA(final_pattern, timeperiod)
        return final_pattern
