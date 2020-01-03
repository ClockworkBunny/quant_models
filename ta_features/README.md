# Notes for TA Features

Check the indicators provided by talib one by one.

## Monmentum Indicators

* **Absolute Price Oscillator**:

    It is not normalized. Fast MA minus Slow MA.

* Ultimate Oscillator:

    Range from 0 to 100

* **AROON**: return two values.

    It is not normalized. Be processed.

* Chande Momentum Oscillaotr

    Range from -100 to 100

* Directional Movement Index

    Range from 0 to 100

* Money Flow Index

    Range from 0 to 100

* Minus Directional Indicator

    Range from 0 to 100

* Plus Directional Indicator

    Range from 0 to 100

* **COMMODITY Channel Index**:

    CCI = [typical price - MA]/ (0.15 * mean deviation)

* Relative Strength Index:

    Range from 0 to 100

* Average Directional Movement Index Rating:

    Range from 0 to 100

* Williams R:

    Range from -100 to 0

* **Momentum**:

    $m=V-V_x$

* Balance of Power

    Range from -1 to 1

## Volatility Indicators

* Normalized Average True Range

    Range from 0 to 1. The eq is $\frac{atr}{close}$

* **Average True Range**

* **True Range**

## Cycle Indicators

* HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period

    Range from 0 to 360

* HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase

    Range from -360 to 360

* **HT_PHASOR** - Hilbert Transform - Phasor Components

    return two values

* **HT_SINE** - Hilbert Transform - SineWave

    return two values

* HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode

    Binary Var: 0 and 1
