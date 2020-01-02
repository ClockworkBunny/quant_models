"""
Inhouse Wrappers for Indicators
"""
import pandas as pd
import numpy as np

class Factor():
    def __init__(self, name, caller, params=[], kwparams={}, outname=[]):
        self._caller = caller
        self._name = name
        self._outname = outname
        self.params = params
        self.kwparams = pd.DataFrame(kwparams)

    def __call__(self, df, *params, **kwparams):
        tmp = self._caller(df, *params, **kwparams)
        if len(self._outname) > 0:
            tmp = pd.DataFrame(np.array(tmp).T)
            tmp.columns = self._outname
        else:
            tmp = pd.DataFrame(np.array(tmp).T)
            tmp.columns = ['out_%02d' % i for i in range(tmp.shape[1])]
        return tmp

    def __repr__(self):
        return self._name

    def set_params_grid(self, grid):
        pass

    def _reorder_kw(self):
        self.kwparams = self.kwparams.reindex(
            sorted(self.kwparams.columns), axis=1)

    def _params_to_kw(self):
        df = pd.DataFrame(self.params)
        df.columns = ['_arg_%02d' % i for i in range(df.shape[1])]
        if len(self.kwparams) > 0:
            self.kwparams = df.merge(self.kwparams, left_index=True,
                                     right_index=True)
        else:
            self.kwparams = df
        self._reorder_kw()
        self.params = []

    def set_kwparams(self, kwparams):
        self.kwparams = pd.DataFrame(kwparams)

    def run(self, df):
        if len(self.params) == 0 and len(self.kwparams) == 0:
            raise RuntimeError('No parameters are given in the class.')

        if len(self.params) > 0:
            self._params_to_kw()

        argcol = self.kwparams.columns.str.match('_arg_[0-9]{2}')
        argdf = self.kwparams.loc[:, argcol].values
        kwdf = self.kwparams.loc[:, ~argcol]
        outlist = []
        for rowid in range(self.kwparams.shape[0]):
            tmpname = self._outname
            if len(tmpname) > 0:
                self._outname = [i + '_%03d' % rowid for i in tmpname]
            outlist.append(self.__call__(
                df, *list(argdf[rowid]),
                **kwdf.iloc[rowid, :].to_dict()))
            self._outname = tmpname

        return outlist



