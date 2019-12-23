# Projects for Quant
Some code sinppet for quant trading with a foucs on machine learning applications. This project is referred to the following resources:

1. The book: [advances in financial machine learning](https://www.amazon.com/Advances-Financial-Machine-Learning-Marcos/dp/1119482089)

2. Git repo: [mlfinlab](https://github.com/hudson-and-thames/mlfinlab) project

3. Basic dataformat: the input data format is a pandas dataframe with the datetime index. And it should be ordered by the time. At the same time, it has ohlcv format.

4. The folder ```TestingNotebooks``` have all the ipython notebooks that contain the testing logics:
    * utils functions
    * info-driven bar
    * Probabilistic of backtesting overfitting
    * Testing Sharpe

#### CustomBar Projects
Sample financial data to create alternative bar data. Conventional bars sampled by time interval may have the following drawbacks:

1. oversample information during low-activity periods and undersample information during high-activity periods
2. exhibit poor statistical properties such as serial correlation, non-normality of returns.

Therefore, some information-driven bars are proposed. The intuitive idea is that we are going to look at other information such as volume, price instead of the time axis.

#### Probability of Backtest Overfitting
How to quantify the probabilitiy of a group of trading strategies that may be overfitted. This project is modified from the [repo](https://github.com/esvhd/pypbo)

#### Triple-bar Labeling


#### Utils Module
Supported features:

1. Utils
    * sample the bar data based on the time index
    * change the timezone of the time index
    * Compute daily vol. given input bar

2. fast_ewma

    using numba to speed up the ewma computation process

3. metrics

    contain lists of metrics that evaluates the trading performance
    * Adjusted Sharpe
    * Non-IID Sharpe
    * Deflated Sharpe Ratio

4. multiprocess

    parallel computation