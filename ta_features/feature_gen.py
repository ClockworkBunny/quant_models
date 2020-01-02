"""
==============================================
Code for prepare features for CNA BS Model
Author: Zhao Rui, Quant Research, Harveston
==============================================
"""
import pandas as pd
import config as conf
from gf1 import gf1


if __name__ == '__main__':
    raw_fea = pd.read_hdf(conf.data_fn + 'fea_data/bs_data.h5')
    raw_fea.reset_index(drop=True, inplace=True)
    df_fea = raw_fea.groupby('symbol').apply(gf1)
    print(df_fea.columns)
    df_fea.reset_index(inplace=True, drop=True)
    df_fea['date'] = raw_fea.date
    df_fea['symbol'] = raw_fea.symbol
    df_fea.head()
    df_fea.to_hdf(conf.data_fn + "fea_data/bs_training.h5",
                '/xgbfea',
                complib='blosc',
                complevel=9)
    

