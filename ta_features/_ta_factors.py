"""
Inhouse Wrappers for Indicators
"""
import pandas as pd
import numpy as np
import talib
from ._base_factors import Factor

class TAFactor(Factor):
    KNOWN_FACTORS = ['RSI', 'CCI', 'ADX', 'ADXR', 'APO', 'AROON', 'AROONOSC',
                     'BOP', 'CMO', 'DX', 'MACD', 'MACDEXT', 'MACDFIX',
                     'MFI', 'MINUS_DI', 'MINUS_DM', 'MOM', 'PLUS_DI',
                     'PLUS_DM', 'PPO', 'ROC', 'ROCR', 'STOCH', 'STOCHF', 'FROC',
                     'STOCHRSI', 'TRIX', 'ULTOSC', 'WILLR', 'BBANDS',
                     'DEMA', 'EMA', 'HT_TRENDLINE', 'KAMA', 'MA', 'MAMA',
                     'MAVP', 'MIDPOINT', 'MIDPRICE', 'SAR', 'SAREXT', 'T3',
                     'TEMA', 'TRIMA', 'WMA', 'CORREL', 'LINEARREG_SLOPE',
                     'STDDEV', 'TSF', 'ATR', 'NATR', 'TRANGE', 'AD', 'ADOSC', 'OBV',
                     'SMA', 'LINEARREG', 'LINEARREG_INTERCEPT', 'MAX', 'MIN', 'ZSCORE']

    def __init__(self, name, map_dict={}, params=[], kwparams={}, outname=[]):
        if name in self.KNOWN_FACTORS:
            CALLER_MAP = {'RSI': [self.RSI_factor, ['RSI']],
                          'CCI': [self.CCI_factor, ['CCI']],
                          'ADX': [self.ADX_factor, ['ADX']],
                          'ADXR': [self.ADXR_factor, ['ADXR']],
                          'APO': [self.APO_factor, ['APO']],
                          'AROON': [self.AROON_factor, ['AROON_Down', 'AROON_Up']],
                          'AROONOSC': [self.AROONOSC_factor, ['AROONOSC']],
                          'BOP': [self.BOP_factor, ['BOP']],
                          'CMO': [self.CMO_factor, ['CMO']],
                          'DX': [self.DX_factor, ['DX']],
                          'MACD': [self.MACD_factor, ['MACD', 'MACD_Signal', 'MACD_Hist']],
                          'MACDEXT': [self.MACDEXT_factor, ['MACD', 'MACD_Signal', 'MACD_Hist']],
                          'MACDFIX': [self.MACDFIX_factor, ['MACD', 'MACD_Signal', 'MACD_Hist']],
                          'MFI': [self.MFI_factor, ['MFI']],
                          'MINUS_DI': [self.MINUS_DI_factor, ['MINUS_DI']],
                          'MINUS_DM': [self.MINUS_DM_factor, ['MINUS_DM']],
                          'MOM': [self.MOM_factor, ['MOM']],
                          'PLUS_DI': [self.PLUS_DI_factor, ['PLUS_DI']],
                          'PLUS_DM': [self.PLUS_DM_factor, ['PLUS_DM']],
                          'PPO': [self.PPO_factor, ['PPO']],
                          'ROC': [self.ROC_factor, ['ROC']],
                          'FROC': [self.FROC_factor, ['FROC']],
                          'ROCR': [self.ROCR_factor, ['ROCR']],
                          'STOCH': [self.STOCH_factor, ['STOCH_slowk', 'STOCH_slowd']],
                          'STOCHF': [self.STOCHF_factor, ['STOCHF_fastk', 'STOCHF_fastd']],
                          'STOCHRSI': [self.STOCHRSI_factor, ['STOCHRSI_fastk', 'STOCHRSI_fastd']],
                          'TRIX': [self.TRIX_factor, ['TRIX']],
                          'ULTOSC': [self.ULTOSC_factor, ['ULTOSC']],
                          'WILLR': [self.WILLR_factor, ['WILLR']],
                          'BBANDS': [self.BBANDS_factor, ['BBANDS_upper', 'BBANDS_middle', 'BBANDS_lower']],
                          'DEMA': [self.DEMA_factor, ['DEMA']],
                          'EMA': [self.EMA_factor, ['EMA']],
                          'HT_TRENDLINE': [self.HT_TRENDLINE_factor, ['HT_TRENDLINE']],
                          'KAMA': [self.KAMA_factor, ['KAMA']],
                          'MA': [self.MA_factor, ['MA']],
                          'MAMA': [self.MAMA_factor, ['MAMA', 'MAMA_fama']],
                          'MAVP': [self.MAVP_factor, ['MAVP']],
                          'MIDPOINT': [self.MIDPOINT_factor, ['MIDPOINT']],
                          'MIDPRICE': [self.MIDPRICE_factor, ['MIDPRICE']],
                          'SAR': [self.SAR_factor, ['SAR']],
                          'SAREXT': [self.SAREXT_factor, ['SAREXT']],
                          'T3': [self.T3_factor, ['T3']],
                          'TEMA': [self.TEMA_factor, ['TEMA']],
                          'TRIMA': [self.TRIMA_factor, ['TRIMA']],
                          'WMA': [self.WMA_factor, ['WMA']],
                          'CORREL': [self.CORREL_factor, ['CORREL']],
                          'LINEARREG_SLOPE': [self.LINEARREG_SLOPE_factor, ['LINEARREG_SLOPE']],
                          'STDDEV': [self.STDDEV_factor, ['STDDEV']],
                          'TSF': [self.TSF_factor, ['TSF']],
                          'ATR': [self.ATR_factor, ['ATR']],
                          'NATR': [self.NATR_factor, ['NATR']],
                          'TRANGE': [self.TRANGE_factor, ['TRANGE']],
                          'AD': [self.AD_factor, ['AD']],
                          'ADOSC': [self.ADOSC_factor, ['ADOSC']],
                          'OBV': [self.OBV_factor, ['OBV']],
                          'SMA': [self.SMA_factor, ['SMA']],
                          'LINEARREG': [self.LINEARREG_factor, ['LINEARREG']],
                          'LINEARREG_INTERCEPT': [self.LINEARREG_INTERCEPT_factor, ['LINEARREG_INTERCEPT']],
                          'MAX': [self.MAX_factor, ['MAX']],
                          'MIN': [self.MIN_factor, ['MIN']],
                          'ZSCORE': [self.ZSCORE_factor, ['ZSCORE']]
                          }
            caller = CALLER_MAP[name][0]
            if len(outname) > 0:
                super(TAFactor, self).__init__(
                    name, caller, params, kwparams, outname)
            else:
                super(TAFactor, self).__init__(
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

    def RSI_factor(self, df, timeperiod=14):
        return talib.RSI(df.loc[:, self.map_dict['default']].values,
                         timeperiod)

    def CMO_factor(self, df, timeperiod=14):
        return talib.CMO(df.loc[:, self.map_dict['default']].values,
                         timeperiod)

    def TRIX_factor(self, df, timeperiod=30):
        return talib.TRIX(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def DEMA_factor(self, df, timeperiod=30):
        return talib.DEMA(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def EMA_factor(self, df, timeperiod=30):
        return talib.EMA(df.loc[:, self.map_dict['default']].values,
                         timeperiod)

    def KAMA_factor(self, df, timeperiod=30):
        return talib.KAMA(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def TSF_factor(self, df, timeperiod=14):
        return talib.TSF(df.loc[:, self.map_dict['default']].values,
                         timeperiod)

    def MIDPOINT_factor(self, df, timeperiod=14):
        return talib.MIDPOINT(df.loc[:, self.map_dict['default']].values,
                              timeperiod)

    def LINEARREG_SLOPE_factor(self, df, timeperiod=14):
        return talib.LINEARREG_SLOPE(
            df.loc[:, self.map_dict['default']].values,
            timeperiod)

    def MIDPRICE_factor(self, df, timeperiod=14):
        return talib.MIDPRICE(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            timeperiod)

    def CORREL_factor(self, df, timeperiod=14):
        return talib.CORREL(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            timeperiod)

    def TEMA_factor(self, df, timeperiod=30):
        return talib.TEMA(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def TRIMA_factor(self, df, timeperiod=30):
        return talib.TRIMA(df.loc[:, self.map_dict['default']].values,
                           timeperiod)

    def WMA_factor(self, df, timeperiod=30):
        return talib.WMA(df.loc[:, self.map_dict['default']].values,
                         timeperiod)

    def T3_factor(self, df, timeperiod=5, vfactor=0):
        return talib.T3(df.loc[:, self.map_dict['default']].values,
                        timeperiod, vfactor)

    def STDDEV_factor(self, df, timeperiod=5, nbdev=1):
        return talib.STDDEV(df.loc[:, self.map_dict['default']].values,
                            timeperiod, nbdev)

    def SAR_factor(self, df, acceleration=0, maximum=0):
        return talib.SAR(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            acceleration, maximum)

    def SAREXT_factor(self, df, startvalue=0,
                      offsetonreverse=0, accelerationinitlong=0,
                      accelerationlong=0, accelerationmax=0,
                      accelerationinitshort=0, accelerationshort=0,
                      accelerationmaxshort=0):
        return talib.SAREXT(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            startvalue, offsetonreverse, accelerationinitlong,
            accelerationlong, accelerationmax,
            accelerationinitshort, accelerationshort,
            accelerationmaxshort)

    def MAVP_factor(self, df, periods, minperiod=30, maxperiod=30, matype=0):
        return talib.MAVP(df.loc[:, self.map_dict['default']].values,
                          periods, minperiod,
                          maxperiod, matype)

    def MA_factor(self, df, timeperiod=30, matype=0):
        return talib.MA(df.loc[:, self.map_dict['default']].values,
                        timeperiod, matype)

    def MAMA_factor(self, df, fastlimit=0, slowlimit=0):
        return talib.MAMA(df.loc[:, self.map_dict['default']].values,
                          fastlimit, slowlimit)

    def HT_TRENDLINE_factor(self, df):
        return talib.HT_TRENDLINE(df.loc[:, self.map_dict['default']].values)

    def MOM_factor(self, df, timeperiod=14):
        return talib.MOM(df.loc[:, self.map_dict['default']].values,
                         timeperiod)

    def ROC_factor(self, df, timeperiod=10):
        return talib.ROC(df.loc[:, self.map_dict['default']].values,
                         timeperiod)

    def ROCR_factor(self, df, timeperiod=10):
        return talib.ROCR(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def MACDEXT_factor(self, df, fastperiod=12, fastmatype=0,
                       slowperiod=26, slowmatype=0,
                       signalperiod=9, signalmatype=0):
        return talib.MACDEXT(df.loc[:, self.map_dict['default']].values,
                             fastperiod, fastmatype, slowperiod, slowmatype,
                             signalperiod, signalmatype)

    def MACDFIX_factor(self, df, signalperiod=9):
        return talib.MACDFIX(df.loc[:, self.map_dict['default']].values,
                             signalperiod)

    def MACD_factor(self, df, fastperiod=12, slowperiod=26, signalperiod=9):
        return talib.MACD(df.loc[:, self.map_dict['default']].values,
                          fastperiod, slowperiod, signalperiod)

    def CCI_factor(self, df, timeperiod=14):
        return talib.CCI(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def ADX_factor(self, df, timeperiod=14):
        return talib.ADX(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def ADXR_factor(self, df, timeperiod=14):
        return talib.ADXR(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def ATR_factor(self, df, timeperiod=14):
        return talib.ATR(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def NATR_factor(self, df, timeperiod=14):
        return talib.NATR(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def OBV_factor(self, df):
        return talib.OBV(
            df.loc[:, self.map_dict['close']].values,
            df.loc[:, self.map_dict['volume']].values)

    def TRANGE_factor(self, df):
        return talib.TRANGE(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values)

    def AD_factor(self, df):
        return talib.AD(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            df.loc[:, self.map_dict['volume']].values)

    def ADOSC_factor(self, df, fastperiod=3, slowperiod=10):
        return talib.ADOSC(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            df.loc[:, self.map_dict['volume']].values,
            fastperiod, slowperiod)

    def MINUS_DI_factor(self, df, timeperiod=14):
        return talib.MINUS_DI(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def MINUS_DM_factor(self, df, timeperiod=14):
        return talib.MINUS_DM(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            timeperiod)

    def PLUS_DI_factor(self, df, timeperiod=14):
        return talib.PLUS_DI(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def PLUS_DM_factor(self, df, timeperiod=14):
        return talib.PLUS_DM(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            timeperiod)

    def DX_factor(self, df, timeperiod=14):
        return talib.DX(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def APO_factor(self, df, fastperiod=12, slowperiod=26, matype=0):
        return talib.APO(df.loc[:, self.map_dict['default']].values,
                         fastperiod, slowperiod, matype)

    def BBANDS_factor(self, df, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
        return talib.BBANDS(df.loc[:, self.map_dict['default']].values,
                            timeperiod, nbdevup, nbdevdn, matype)

    def PPO_factor(self, df, fastperiod=12, slowperiod=26, matype=0):
        return talib.PPO(df.loc[:, self.map_dict['default']].values,
                         fastperiod, slowperiod, matype)

    def AROON_factor(self, df, timeperiod=14):
        return talib.AROON(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            timeperiod)

    def AROONOSC_factor(self, df, timeperiod=14):
        return talib.AROONOSC(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            timeperiod)

    def BOP_factor(self, df):
        return talib.BOP(
            df.loc[:, self.map_dict['open']].values,
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values)

    def MFI_factor(self, df, timeperiod):
        return talib.MFI(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            df.loc[:, self.map_dict['volume']].values,
            timeperiod)

    def STOCH_factor(self, df, fastk_period=5, slowk_period=3,
                     slowk_matype=0, slowd_period=3, slowd_matype=0):
        return talib.STOCH(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            fastk_period, slowk_period,
            slowk_matype, slowd_period,
            slowd_matype)

    def STOCHF_factor(self, df, fastk_period=5, fastd_period=3,
                      fastd_matype=0):
        return talib.STOCHF(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            fastk_period, fastd_period,
            fastd_matype)

    def STOCHRSI_factor(self, df, timeperiod=14, fastk_period=5,
                        fastd_period=3, fastd_matype=0):
        return talib.STOCHRSI(
            df.loc[:, self.map_dict['default']].values,
            timeperiod, fastk_period, fastd_period,
            fastd_matype)

    def ULTOSC_factor(self, df, timeperiod1=7, timeperiod2=14, timeperiod3=28):
        return talib.ULTOSC(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod1, timeperiod2,
            timeperiod3)

    def WILLR_factor(self, df, timeperiod=14):
        return talib.WILLR(
            df.loc[:, self.map_dict['high']].values,
            df.loc[:, self.map_dict['low']].values,
            df.loc[:, self.map_dict['close']].values,
            timeperiod)

    def FROC_factor(self, df, timeperiod=10):
        return np.roll(talib.ROC(df.loc[:, self.map_dict['default']].values,
                                 timeperiod), -timeperiod)

    def SMA_factor(self, df, timeperiod=14):
        return talib.SMA(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def LINEARREG_factor(self, df, timeperiod=14):
        return talib.LINEARREG(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def LINEARREG_INTERCEPT_factor(self, df, timeperiod=14):
        return talib.LINEARREG_INTERCEPT(df.loc[:, self.map_dict['default']].values,
                          timeperiod)
    def MAX_factor(self, df, timeperiod=14):
        return talib.MAX(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def MIN_factor(self, df, timeperiod=14):
        return talib.MIN(df.loc[:, self.map_dict['default']].values,
                          timeperiod)

    def ZSCORE_factor(self, df, timeperiod=14):
        std = talib.STDDEV(df.loc[:, self.map_dict['default']].values, timeperiod)
        avr = talib.SMA(df.loc[:, self.map_dict['default']].values,
                          timeperiod)
        return np.divide(np.subtract(df.loc[:, self.map_dict['default']].values,avr),std)

if __name__ == '__main__':
    #    def rsi_factor(df, timeperiod=14):
    #        return talib.RSI(df.close.values, timeperiod)
    #
    #    def cci_factor(df, timeperiod):
    #        return talib.CCI(df.high.values, df.low.values, df.close.values, timeperiod)
    #    rsi = Factor("RSI", rsi_factor, kwparams={
    #                 'timeperiod': [14, 20, 30, 100, 200]})
    #    cci = Factor("CCI", cci_factor, [[14], [20], [30], [100], [200]])
    stoch = TAFactor('STOCH', kwparams={'fastk_period': [
                     9, 9, 9, 5, 5, 5], 'slowk_period': [6, 3, 2, 4, 3, 2]})
