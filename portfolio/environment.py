import numpy as np
import pandas as pd


class EquityEnvironment:
    def __init__(self, inputdf, capital = 1e6):
        self.capital = capital
        self.data    = inputdf

    def preprocess_state(self, state):
        """add the logic that remove the all-zero returns"""
        zero_cols = (state == 0).all()
        new_state  = state.loc[:,~zero_cols]
        if new_state.shape[1] != state.shape[1]:
            print('remove the zero returns of stocks')
            print(set(state.columns.tolist()) - set(new_state.columns.tolist()))
            removal_label = True
        else:
            removal_label  = False
        return new_state, removal_label

    def get_state(self, t, lookback, is_cov_matrix = True, is_raw_time_series = False, is_fit = True):
        """
        # args:
        1. t: the ending lindex,  t-lookback: the start index
        2. is_cov_matrix: boolean.
        return the covariance matrix True else return the return series
        3. is_raw_time_series: boolean.
        true indicates the input df is the return series
        flase indicates the input df is the price series
        4. is_fit:
        true indicates the input df is for weights computation, which do not allow for all zero returns i.e. whole columne
        else indicates means no filter
        """
        assert lookback <= t
        decision_making_state = self.data.iloc[t-lookback:t]
        decision_making_state = decision_making_state.pct_change().dropna()

        if is_cov_matrix:
            x = decision_making_state.cov()
            return x, False
        else:
            if is_raw_time_series:
                decision_making_state = self.data.iloc[t-lookback:t]
        if is_fit:
            return self.preprocess_state(decision_making_state)
        else:
            return decision_making_state, False

    def get_reward(self, action, action_t, reward_t, alpha = 0.01):
        def local_portfolio(returns, weights):
            weights = np.array(weights)
            rets = returns.mean() # * 252
            covs = returns.cov() # * 252
            P_ret = np.sum(rets * weights)
            P_vol = np.sqrt(np.dot(weights.T, np.dot(covs, weights)))
            P_sharpe = P_ret / P_vol
            return np.array([P_ret, P_vol, P_sharpe])

        data_period = self.data[action_t:reward_t]
        weights = action
        returns = data_period.pct_change().dropna()
        sharpe = local_portfolio(returns, weights)[-1]
        sharpe = np.array([sharpe] * len(self.data.columns))
        rew = (data_period.values[-1] - data_period.values[0]) / data_period.values[0]

        return np.dot(returns, weights), rew



