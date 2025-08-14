# 📋 OpenAlgo Technical Indicators - Complete Function List

This document provides a comprehensive list of all available indicator functions in the OpenAlgo Technical Analysis Library.

## 🚀 Usage

```python
from openalgo import ta

# All functions are accessed through the ta object
result = ta.function_name(parameters)
```

---

## 🔵 TREND INDICATORS (19 Functions)

### Basic Moving Averages
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.sma(data, period)` | Simple Moving Average | data, period | Array |
| `ta.ema(data, period)` | Exponential Moving Average | data, period | Array |
| `ta.wma(data, period)` | Weighted Moving Average | data, period | Array |

### Advanced Moving Averages  
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.dema(data, period)` | Double Exponential MA | data, period | Array |
| `ta.tema(data, period)` | Triple Exponential MA | data, period | Array |
| `ta.hma(data, period)` | Hull Moving Average | data, period | Array |
| `ta.vwma(data, volume, period)` | Volume Weighted MA | data, volume, period | Array |
| `ta.alma(data, period=21, offset=0.85, sigma=6.0)` | Arnaud Legoux MA | data, period, offset, sigma | Array |
| `ta.kama(data, period=10, fast_period=2, slow_period=30)` | Kaufman's Adaptive MA | data, period, fast_period, slow_period | Array |
| `ta.zlema(data, period)` | Zero Lag Exponential MA | data, period | Array |
| `ta.t3(data, period=21, v_factor=0.7)` | T3 Moving Average | data, period, v_factor | Array |
| `ta.frama(data, period=16)` | Fractal Adaptive MA | data, period | Array |
| `ta.trima(data, period)` | Triangular Moving Average | data, period | Array |
| `ta.mcginley_dynamic(data, period=14)` | McGinley Dynamic | data, period | Array |
| `ta.vidya(data, period=14, alpha=0.2)` | Variable Index Dynamic Average | data, period, alpha | Array |

### Complex Trend Systems
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.supertrend(high, low, close, period=10, multiplier=3.0)` | Supertrend | high, low, close, period, multiplier | (values, direction) |
| `ta.ichimoku(high, low, close, tenkan=9, kijun=26, senkou_b=52, displacement=26)` | Ichimoku Cloud | high, low, close, tenkan, kijun, senkou_b, displacement | (tenkan, kijun, span_a, span_b, chikou) |
| `ta.alligator(high, low, jaw_period=13, jaw_shift=8, teeth_period=8, teeth_shift=5, lips_period=5, lips_shift=3)` | Bill Williams Alligator | high, low, jaw_period, jaw_shift, teeth_period, teeth_shift, lips_period, lips_shift | (jaw, teeth, lips) |
| `ta.ma_envelopes(data, period=20, percentage=2.5, ma_type='SMA')` | Moving Average Envelopes | data, period, percentage, ma_type | (upper, middle, lower) |

---

## 🟡 MOMENTUM INDICATORS (9 Functions)

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.rsi(data, period=14)` | Relative Strength Index | data, period | Array |
| `ta.macd(data, fast_period=12, slow_period=26, signal_period=9)` | MACD | data, fast_period, slow_period, signal_period | (macd, signal, histogram) |
| `ta.stochastic(high, low, close, k_period=14, d_period=3)` | Stochastic Oscillator | high, low, close, k_period, d_period | (k_percent, d_percent) |
| `ta.cci(high, low, close, period=20)` | Commodity Channel Index | high, low, close, period | Array |
| `ta.williams_r(high, low, close, period=14)` | Williams %R | high, low, close, period | Array |
| `ta.bop(open, high, low, close)` | Balance of Power | open, high, low, close | Array |
| `ta.elderray(high, low, close, period=13)` | Elder Ray Index | high, low, close, period | (bull_power, bear_power) |
| `ta.fisher(data, period=10)` | Fisher Transform | data, period | (fisher, trigger) |
| `ta.crsi(data, rsi_period=3, streak_period=2, roc_period=100)` | Connors RSI | data, rsi_period, streak_period, roc_period | Array |

---

## 🟠 OSCILLATORS (22 Functions)

### Basic Oscillators
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.roc_oscillator(data, period=12)` | Rate of Change | data, period | Array |
| `ta.cmo(data, period=14)` | Chande Momentum Oscillator | data, period | Array |
| `ta.trix(data, period=14)` | TRIX | data, period | Array |
| `ta.uo_oscillator(high, low, close, period1=7, period2=14, period3=28)` | Ultimate Oscillator | high, low, close, period1, period2, period3 | Array |
| `ta.awesome_oscillator(high, low, fast_period=5, slow_period=34)` | Awesome Oscillator | high, low, fast_period, slow_period | Array |
| `ta.accelerator_oscillator(high, low, period=5)` | Accelerator Oscillator | high, low, period | Array |
| `ta.ppo(data, fast_period=12, slow_period=26, signal_period=9)` | Percentage Price Oscillator | data, fast_period, slow_period, signal_period | (ppo, signal, histogram) |
| `ta.price_oscillator(data, fast_period=10, slow_period=20, ma_type='SMA')` | Price Oscillator | data, fast_period, slow_period, ma_type | Array |
| `ta.dpo(data, period=20)` | Detrended Price Oscillator | data, period | Array |
| `ta.aroon_oscillator(high, low, period=25)` | Aroon Oscillator | high, low, period | Array |

### Advanced Oscillators
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.stochrsi(data, rsi_period=14, stoch_period=14, k_period=3, d_period=3)` | Stochastic RSI | data, rsi_period, stoch_period, k_period, d_period | (k_percent, d_percent) |
| `ta.rvi(open, high, low, close, period=10)` | Relative Vigor Index | open, high, low, close, period | (rvi, signal) |
| `ta.cho(high, low, close, volume, fast_period=3, slow_period=10)` | Chaikin Oscillator | high, low, close, volume, fast_period, slow_period | Array |

### Advanced Oscillators
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.chop(high, low, close, period=14)` | Choppiness Index | high, low, close, period | Array |
| `ta.kst(close, roc1=10, roc2=15, roc3=20, roc4=30, sma1=10, sma2=10, sma3=10, sma4=15, signal_period=9)` | Know Sure Thing | close, roc1-4, sma1-4, signal_period | (kst, signal) |
| `ta.tsi(close, long_period=25, short_period=13, signal_period=13)` | True Strength Index | close, long_period, short_period, signal_period | (tsi, signal) |
| `ta.vi(high, low, close, period=14)` | Vortex Indicator | high, low, close, period | (vi_plus, vi_minus) |
| `ta.stc(close, fast_period=23, slow_period=50, cycle_period=10, d1_period=3, d2_period=3)` | Schaff Trend Cycle | close, fast_period, slow_period, cycle_period, d1_period, d2_period | Array |
| `ta.gator_oscillator(high, low, jaw_period=13, jaw_shift=8, teeth_period=8, teeth_shift=5, lips_period=5, lips_shift=3)` | Gator Oscillator | high, low, jaw_period, jaw_shift, teeth_period, teeth_shift, lips_period, lips_shift | (upper_gator, lower_gator) |

---

## 🔴 VOLATILITY INDICATORS (23 Functions)

### Basic Volatility
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.atr(high, low, close, period=14)` | Average True Range | high, low, close, period | Array |
| `ta.true_range(high, low, close)` | True Range | high, low, close | Array |
| `ta.natr(high, low, close, period=14)` | Normalized ATR | high, low, close, period | Array |
| `ta.stddev(data, period=20)` | Standard Deviation | data, period | Array |
| `ta.variance(data, period=20)` | Variance | data, period | Array |

### Channel & Band Indicators
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.bbands(data, period=20, std_dev=2.0)` | Bollinger Bands | data, period, std_dev | (upper, middle, lower) |
| `ta.keltner_channel(high, low, close, ema_period=20, atr_period=10, multiplier=2.0)` | Keltner Channel | high, low, close, ema_period, atr_period, multiplier | (upper, middle, lower) |
| `ta.donchian_channel(high, low, period=20)` | Donchian Channel | high, low, period | (upper, middle, lower) |

### Advanced Volatility
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.chaikin_volatility(high, low, ema_period=10, roc_period=10)` | Chaikin Volatility | high, low, ema_period, roc_period | Array |
| `ta.rvi_volatility(data, stdev_period=10, rsi_period=14)` | Relative Volatility Index | data, stdev_period, rsi_period | Array |
| `ta.mass_index(high, low, fast_period=9, slow_period=25)` | Mass Index | high, low, fast_period, slow_period | Array |

### Advanced Volatility Indicators
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.bbands_percent_b(close, period=20, std_dev=2)` | Bollinger Bands %B | close, period, std_dev | Array |
| `ta.bbands_bandwidth(close, period=20, std_dev=2)` | Bollinger Bandwidth | close, period, std_dev | Array |
| `ta.chandelier_exit(high, low, close, period=22, multiplier=3.0)` | Chandelier Exit | high, low, close, period, multiplier | (long_exit, short_exit) |
| `ta.hv(close, period=20, annualize=True)` | Historical Volatility | close, period, annualize | Array |
| `ta.ulcer_index(close, period=14)` | Ulcer Index | close, period | Array |
| `ta.starc_bands(high, low, close, ma_period=20, atr_period=15, multiplier=2.0)` | STARC Bands | high, low, close, ma_period, atr_period, multiplier | (upper, middle, lower) |

---

## 🟣 VOLUME INDICATORS (13 Functions)

### Basic Volume
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.obv(close, volume)` | On Balance Volume | close, volume | Array |
| `ta.vwap(high, low, close, volume, period=0)` | Volume Weighted Average Price | high, low, close, volume, period | Array |
| `ta.adl(high, low, close, volume)` | Accumulation/Distribution Line | high, low, close, volume | Array |
| `ta.force_index(close, volume)` | Force Index | close, volume | Array |

### Advanced Volume
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.mfi(high, low, close, volume, period=14)` | Money Flow Index | high, low, close, volume, period | Array |
| `ta.cmf(high, low, close, volume, period=20)` | Chaikin Money Flow | high, low, close, volume, period | Array |
| `ta.emv(high, low, volume, scale=1000000)` | Ease of Movement | high, low, volume, scale | Array |
| `ta.nvi(close, volume)` | Negative Volume Index | close, volume | Array |
| `ta.pvi(close, volume)` | Positive Volume Index | close, volume | Array |
| `ta.volume_oscillator(volume, fast_period=5, slow_period=10)` | Volume Oscillator | volume, fast_period, slow_period | Array |
| `ta.vroc(volume, period=25)` | Volume Rate of Change | volume, period | Array |
| `ta.kvo(high, low, close, volume, fast_period=34, slow_period=55)` | Klinger Volume Oscillator | high, low, close, volume, fast_period, slow_period | Array |
| `ta.pvt(close, volume)` | Price Volume Trend | close, volume | Array |

---

## 🟤 STATISTICAL INDICATORS (8 Functions)

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.linear_regression(data, period=14)` | Linear Regression | data, period | Array |
| `ta.linear_regression_slope(data, period=14)` | Linear Regression Slope | data, period | Array |
| `ta.correlation(data1, data2, period=20)` | Pearson Correlation | data1, data2, period | Array |
| `ta.beta(asset, market, period=252)` | Beta Coefficient | asset, market, period | Array |
| `ta.variance(data, period=20)` | Variance | data, period | Array |
| `ta.time_series_forecast(data, period=14)` | Time Series Forecast | data, period | Array |
| `ta.median(data, period=20)` | Rolling Median | data, period | Array |
| `ta.mode(data, period=20, bins=10)` | Rolling Mode | data, period, bins | Array |

---

## ⚫ HYBRID & ADVANCED INDICATORS (10 Functions)

### Directional & Trend Systems
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.adx_system(high, low, close, period=14)` | ADX System | high, low, close, period | (di_plus, di_minus, adx) |
| `ta.aroon_system(high, low, period=25)` | Aroon System | high, low, period | (aroon_up, aroon_down) |
| `ta.directional_movement(high, low, close, period=14)` | Directional Movement | high, low, close, period | (di_plus, di_minus) |

### Support/Resistance Systems
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.pivot_points(high, low, close)` | Pivot Points | high, low, close | (pivot, r1, s1, r2, s2, r3, s3) |
| `ta.parabolic_sar(high, low, acceleration=0.02, maximum=0.2)` | Parabolic SAR | high, low, acceleration, maximum | (sar, trend) |
| `ta.psar(high, low, acceleration=0.02, maximum=0.2)` | PSAR Values Only | high, low, acceleration, maximum | Array |

### Advanced Technical Systems
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.hilbert_trendline(data)` | Hilbert Transform Trendline | data | Array |

### Advanced Pattern Recognition
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.zigzag(high, low, deviation=5.0)` | Zig Zag | high, low, deviation | Array |
| `ta.williams_fractals(high, low, period=2)` | Williams Fractals | high, low, period | (fractal_high, fractal_low) |
| `ta.random_walk_index(high, low, close, period=14)` | Random Walk Index | high, low, close, period | (rwi_high, rwi_low) |

---

## ⚪ UTILITY FUNCTIONS (7 Functions)

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `ta.crossover(series1, series2)` | Series Crossover Detection | series1, series2 | Boolean Array |
| `ta.crossunder(series1, series2)` | Series Crossunder Detection | series1, series2 | Boolean Array |
| `ta.highest(data, period)` | Highest Value | data, period | Array |
| `ta.lowest(data, period)` | Lowest Value | data, period | Array |
| `ta.change(data, length=1)` | Change in Value | data, length | Array |
| `ta.roc(data, length)` | Rate of Change Utility | data, length | Array |
| `ta.stdev(data, period)` | Standard Deviation Utility | data, period | Array |

---

## 📊 SUMMARY STATISTICS

| Category | Function Count | Description |
|----------|----------------|-------------|
| **Trend Indicators** | 19 | Moving averages and trend-following systems |
| **Momentum Indicators** | 9 | Price momentum and strength indicators |
| **Oscillators** | 22 | Bounded oscillators and momentum tools |
| **Volatility Indicators** | 23 | Price volatility and range measurements |
| **Volume Indicators** | 13 | Volume analysis and flow indicators |
| **Statistical Indicators** | 8 | Mathematical and statistical tools |
| **Hybrid Indicators** | 10 | Multi-faceted analysis systems |
| **Utility Functions** | 7 | Helper and calculation functions |
| **TOTAL** | **100** | **Complete technical analysis toolkit** |

---

## 🎯 Quick Reference Examples

```python
from openalgo import ta
import numpy as np

# Sample data
close = np.random.randn(100) + 100
high = close + np.random.rand(100)
low = close - np.random.rand(100)  
volume = np.random.randint(1000, 10000, 100)

# Trend Analysis
sma_20 = ta.sma(close, 20)
ema_50 = ta.ema(close, 50)
supertrend, direction = ta.supertrend(high, low, close, 10, 3)

# Momentum Analysis  
rsi = ta.rsi(close, 14)
macd_line, signal, histogram = ta.macd(close, 12, 26, 9)

# Volatility Analysis
atr = ta.atr(high, low, close, 14)
upper, middle, lower = ta.bbands(close, 20, 2)

# Volume Analysis
obv = ta.obv(close, volume)
mfi = ta.mfi(high, low, close, volume, 14)

# Advanced Analysis
di_plus, di_minus, adx = ta.adx_system(high, low, close, 14)
chop = ta.chop(high, low, close, 14)
```

---

## 📚 Additional Resources

- **Complete Documentation**: See `TECHNICAL_INDICATORS_GUIDE.md`
- **Parameter Reference**: See `PARAMETERS_REFERENCE.md`
- **Quick Reference**: See `INDICATORS_QUICK_REFERENCE.md`
- **Usage Examples**: See `examples/` directory

---

*Last Updated: August 2025*
*OpenAlgo Technical Indicators Library v2.0+*