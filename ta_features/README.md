# Notes for TA Features

Basically, in this folder, three kinds of ta features are provided:

1. **Original TA Features**:

Some TA factors which are normalized already such as RSI. The class is in `_ta_factors.py`.

2. **Normalized TA Features**:

Some TA factors are normalized in this class. The class is in `_nta_factors.py`.

3. **Pattern Counting Features**:

Based on traditional pattern recognition factors, we count how many buy signal happen and how many sell signal happe. EMA is applied for a given lookback period. The class is in `_patterns_factors.py`.

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
