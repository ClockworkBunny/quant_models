import pandas as pd
import numpy as np

class LS_Test:
    """
    The class that help the development of LS strategy, which is mainly focused on PNL computation
    """

    def __init__(self, N=2, rank_descend=True):
        """
        Constructor, two important arguments should be passed

        # args
            threshold : the sampling threshold
            if it is int type, it will be absolute number of stocks
            if float, it will be relative percentage of stocks for selection
            dictcol : dict that map col names to defined col names (datetime, price, volume)
        """
        # Base properties
        self.N   = N
        self.rank_descend = rank_descend
        self.df_inds   = []
        self.df_exeps  = []
        self.all_ind   = None
        self.all_exep  = None

    def load_data(self, df_indlist, df_exepslist):
    """
    for df_indlist: each element is a dataframe having the indicator value for one index/equity.
        1.The index is "datetime" in pd.datetime type
        2.The column name is indicator_{}.format(idx in list)

    The corresponding list is df_exepslist, each element is a dataframe having the exe price for one index/equity.
        1.The index is "datetime" in pd.datetime type
        2.The column name is indicator_{}.format(idx in list)
    """
        self.df_inds  = df_indlist
        self.df_exeps = df_exepslist

    def align_data(self):
        """
        union the dataframe from price and indicators
        """
        all_ind = self.df_inds[0].copy()
        all_exep = self.df_exeps[0].copy()
        for idx in range(1, len(self.df_inds)):
            all_ind = all_ind.merge(self.df_inds[idx], how='outer', on='datetime')
            all_exep = all_exep.merge(self.df_exeps[idx], how='outer', on='datetime')
        # merge will disorder
        all_ind.sort_index(inplace=True)
        all_ind.fillna(method='ffill', inplace=True)
        all_ind.dropna(inplace=True)
        all_exep.sort_index(inplace=True)
        all_exep.fillna(method='ffill', inplace=True)
        all_exep.dropna(inplace=True)
        assert(all_exep.shape[0]==all_ind.shape[0])
        self.all_ind = all_ind
        self.all_exep = all_exep
        return all_ind, all_exep

    def gen_buysell(self):
        """
        generator buy sell point based on ranking
        """
        if type(self.N) == int:
            used_num = self.N
        else:
            used_num = int(self.N * all_bs.shape[1])
        all_bs = self.all_ind.copy()
        for idx in range(all_bs.shape[0]):
            ind_array = self.all_ind.iloc[idx].values
            all_bs.iloc[idx] = 0
            indices_ranked = np.argsort(ind_array)
            if self.rank_descend:
                indices_ranked = indices_ranked[::-1]
            long_indices  = indices_ranked[-used_num:]
            short_indices = indices_ranked[:used_num]
            all_bs.iloc[idx, long_indices]  = 1
            all_bs.iloc[idx, short_indices] = -1
        return all_bs

    def gen_pnl(self, all_bs):
        """
        based on buysell points, compute the pnl of the whole portfoilo
        return the whole portfoilo daily pnl,  each individual equity pnl
        """
        for idx in range(len(self.df_inds)):
            self.all_exep['rt_{}'.format(idx)] = self.all_exep['exep_{}'.format(idx)].pct_change()
            self.all_exep['rt_{}'.format(idx)] = self.all_exep['rt_{}'.format(idx)].shift(-1)
        all_pnl = self.all_exep.fillna(0)
        for idx in range(len(self.df_inds)):
            all_pnl['lsrt_{}'.format(idx)] = all_pnl['rt_{}'.format(idx)] * all_bs['indicator_{}'.format(idx)]
        all_pnl         = all_pnl.loc[:, all_pnl.column.str.contains('lsrt')]
        all_pnl_idv     = all_pnl.copy()
        all_pnl['lsrt'] = all_pnl.sum(axis=1)
    return all_pnl[['lsrt']], all_pnl_idv

