# OpenAlgo Technical Indicators - Quick Reference

## Installation & Import

```python
pip install openalgo
```

```python
from openalgo import ta
import numpy as np
```

## Indicators by Category

### 📈 Trend Indicators (20)

**Legend:** 🔴 Required | 🟢 Optional (with default)

| Indicator | Function | Parameters | Returns | Example |
|-----------|----------|------------|---------|---------|
| Simple Moving Average | `ta.sma(data, period)` | 🔴 data, 🔴 period | Array | `sma_20 = ta.sma(close, 20)` |
| Exponential Moving Average | `ta.ema(data, period)` | 🔴 data, 🔴 period | Array | `ema_50 = ta.ema(close, 50)` |
| Weighted Moving Average | `ta.wma(data, period)` | 🔴 data, 🔴 period | Array | `wma_10 = ta.wma(close, 10)` |
| Double EMA | `ta.dema(data, period)` | 🔴 data, 🔴 period | Array | `dema_20 = ta.dema(close, 20)` |
| Triple EMA | `ta.tema(data, period)` | 🔴 data, 🔴 period | Array | `tema_20 = ta.tema(close, 20)` |
| Hull Moving Average | `ta.hma(data, period)` | 🔴 data, 🔴 period | Array | `hma_20 = ta.hma(close, 20)` |
| Volume Weighted MA | `ta.vwma(data, volume, period)` | 🔴 data, 🔴 volume, 🔴 period | Array | `vwma_20 = ta.vwma(close, volume, 20)` |
| Arnaud Legoux MA | `ta.alma(data, period=21, offset=0.85, sigma=6.0)` | 🔴 data, 🟢 period=21, 🟢 offset=0.85, 🟢 sigma=6.0 | Array | `alma = ta.alma(close)` |
| Kaufman Adaptive MA | `ta.kama(data, period=10, fast=2, slow=30)` | 🔴 data, 🟢 period=10, 🟢 fast=2, 🟢 slow=30 | Array | `kama = ta.kama(close)` |
| Zero Lag EMA | `ta.zlema(data, period)` | 🔴 data, 🔴 period | Array | `zlema_20 = ta.zlema(close, 20)` |
| T3 Moving Average | `ta.t3(data, period=21, v_factor=0.7)` | 🔴 data, 🟢 period=21, 🟢 v_factor=0.7 | Array | `t3 = ta.t3(close)` |
| Fractal Adaptive MA | `ta.frama(data, period=16)` | 🔴 data, 🟢 period=16 | Array | `frama = ta.frama(close)` |
| Supertrend | `ta.supertrend(high, low, close, period=10, mult=3.0)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=10, 🟢 mult=3.0 | (values, direction) | `st, dir = ta.supertrend(h, l, c)` |
| Ichimoku Cloud | `ta.ichimoku(high, low, close, tenkan=9, kijun=26, senkou=52, disp=26)` | 🔴 high, 🔴 low, 🔴 close, 🟢 tenkan=9, 🟢 kijun=26, 🟢 senkou=52, 🟢 disp=26 | (tenkan, kijun, span_a, span_b, chikou) | `t, k, sa, sb, c = ta.ichimoku(h, l, c)` |
| Chande Kroll Stop | `ta.ckstop(high, low, close, period=10, mult=1.0)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=10, 🟢 mult=1.0 | (long_stop, short_stop) | `ls, ss = ta.ckstop(h, l, c)` |
| Triangular MA | `ta.trima(data, period)` | 🔴 data, 🔴 period | Array | `trima_20 = ta.trima(close, 20)` |
| McGinley Dynamic | `ta.mcginley(data, period)` | 🔴 data, 🔴 period | Array | `md_14 = ta.mcginley(close, 14)` |
| VIDYA | `ta.vidya(data, period=14, alpha=0.2)` | 🔴 data, 🟢 period=14, 🟢 alpha=0.2 | Array | `vidya = ta.vidya(close)` |
| Alligator | `ta.alligator(data, jaw=13, teeth=8, lips=5)` | 🔴 data, 🟢 jaw=13, 🟢 teeth=8, 🟢 lips=5 | (jaw, teeth, lips) | `j, t, l = ta.alligator(hl2)` |
| MA Envelopes | `ta.ma_envelopes(data, period=20, pct=2.5, ma_type="SMA")` | 🔴 data, 🟢 period=20, 🟢 pct=2.5, 🟢 ma_type | (upper, middle, lower) | `u, m, l = ta.ma_envelopes(close)` |

### 💫 Momentum Indicators (9)

| Indicator | Function | Parameters | Returns | Example |
|-----------|----------|------------|---------|---------|
| RSI | `ta.rsi(data, period=14)` | 🔴 data, 🟢 period=14 | Array (0-100) | `rsi = ta.rsi(close)` |
| MACD | `ta.macd(data, fast=12, slow=26, signal=9)` | 🔴 data, 🟢 fast=12, 🟢 slow=26, 🟢 signal=9 | (macd, signal, histogram) | `m, s, h = ta.macd(close)` |
| Stochastic | `ta.stochastic(high, low, close, k=14, d=3)` | 🔴 high, 🔴 low, 🔴 close, 🟢 k=14, 🟢 d=3 | (k%, d%) | `k, d = ta.stochastic(h, l, c)` |
| CCI | `ta.cci(high, low, close, period=20)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=20 | Array | `cci = ta.cci(high, low, close)` |
| Williams %R | `ta.williams_r(high, low, close, period=14)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=14 | Array (-100 to 0) | `wr = ta.williams_r(h, l, c)` |
| Balance of Power | `ta.bop(open, high, low, close)` | 🔴 open, 🔴 high, 🔴 low, 🔴 close | Array (-1 to 1) | `bop = ta.bop(o, h, l, c)` |
| Elder Ray Index | `ta.elderray(high, low, close, period=13)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=13 | (bull_power, bear_power) | `bull, bear = ta.elderray(h, l, c)` |
| Fisher Transform | `ta.fisher(data, period=10)` | 🔴 data, 🟢 period=10 | (fisher, trigger) | `fish, trig = ta.fisher(close)` |
| Connors RSI | `ta.crsi(data, rsi=3, streak=2, roc=100)` | 🔴 data, 🟢 rsi=3, 🟢 streak=2, 🟢 roc=100 | Array (0-100) | `crsi = ta.crsi(close)` |

### 📊 Volatility Indicators (17)

| Indicator | Function | Parameters | Returns | Example |
|-----------|----------|------------|---------|---------|
| ATR | `ta.atr(high, low, close, period)` | high, low, close, period=14 | Array | `atr_14 = ta.atr(h, l, c, 14)` |
| Bollinger Bands | `ta.bbands(data, period, std)` | data, period=20, std_dev=2 | (upper, middle, lower) | `u, m, l = ta.bbands(close, 20, 2)` |
| Keltner Channel | `ta.keltner_channel(h, l, c, ema, atr, mult)` | high, low, close, ema=20, atr=10, mult=2 | (upper, middle, lower) | `u, m, l = ta.keltner_channel(h, l, c)` |
| Donchian Channel | `ta.donchian_channel(high, low, period)` | high, low, period=20 | (upper, middle, lower) | `u, m, l = ta.donchian_channel(h, l, 20)` |
| Chaikin Volatility | `ta.chaikin_volatility(h, l, ema, roc)` | high, low, ema=10, roc=10 | Array | `cv = ta.chaikin_volatility(h, l, 10, 10)` |
| NATR | `ta.natr(high, low, close, period)` | high, low, close, period=14 | Array (%) | `natr = ta.natr(h, l, c, 14)` |
| RVI | `ta.rvi_volatility(data, std, rsi)` | data, stdev_period=10, rsi_period=14 | Array | `rvi = ta.rvi_volatility(close, 10, 14)` |
| Ultimate Oscillator | `ta.ultimate_oscillator(h, l, c, p1, p2, p3)` | high, low, close, p1=7, p2=14, p3=28 | Array | `uo = ta.ultimate_oscillator(h, l, c)` |
| Standard Deviation | `ta.stddev(data, period)` | data, period=20 | Array | `std = ta.stddev(close, 20)` |
| True Range | `ta.true_range(high, low, close)` | high, low, close | Array | `tr = ta.true_range(h, l, c)` |
| Mass Index | `ta.mass_index(high, low, fast, slow)` | high, low, fast=9, slow=25 | Array | `mi = ta.mass_index(h, l, 9, 25)` |
| Bollinger %B | `ta.bb_percent_b(data, period=20, std_dev=2.0)` | 🔴 data, 🟢 period=20, 🟢 std_dev=2.0 | Array | `bb_pct_b = ta.bb_percent_b(close)` |
| Bollinger Bandwidth | `ta.bb_bandwidth(data, period=20, std_dev=2.0)` | 🔴 data, 🟢 period=20, 🟢 std_dev=2.0 | Array | `bb_bw = ta.bb_bandwidth(close)` |
| Chandelier Exit | `ta.chandelier_exit(h, l, c, period=22, mult=3.0)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=22, 🟢 mult=3.0 | (long_exit, short_exit) | `le, se = ta.chandelier_exit(h, l, c)` |
| Historical Volatility | `ta.hv(data, period=20, annualize=True)` | 🔴 data, 🟢 period=20, 🟢 annualize=True | Array (%) | `hv = ta.hv(close)` |
| Ulcer Index | `ta.ulcer_index(data, period=14)` | 🔴 data, 🟢 period=14 | Array | `ui = ta.ulcer_index(close)` |
| STARC Bands | `ta.starc_bands(h, l, c, ma=20, atr=15, mult=2.0)` | 🔴 high, 🔴 low, 🔴 close, 🟢 ma=20, 🟢 atr=15, 🟢 mult=2.0 | (upper, middle, lower) | `u, m, l = ta.starc_bands(h, l, c)` |

### 📉 Volume Indicators (13)

| Indicator | Function | Parameters | Returns | Example |
|-----------|----------|------------|---------|---------|
| OBV | `ta.obv(close, volume)` | close, volume | Array | `obv = ta.obv(close, volume)` |
| VWAP | `ta.vwap(h, l, c, v, period)` | high, low, close, volume, period=0 | Array | `vwap = ta.vwap(h, l, c, v, 0)` |
| MFI | `ta.mfi(h, l, c, v, period)` | high, low, close, volume, period=14 | Array (0-100) | `mfi = ta.mfi(h, l, c, v, 14)` |
| A/D Line | `ta.adl(high, low, close, volume)` | high, low, close, volume | Array | `adl = ta.adl(h, l, c, v)` |
| Chaikin Money Flow | `ta.cmf(h, l, c, v, period)` | high, low, close, volume, period=20 | Array | `cmf = ta.cmf(h, l, c, v, 20)` |
| Ease of Movement | `ta.emv(high, low, volume, scale)` | high, low, volume, scale=1000000 | Array | `emv = ta.emv(h, l, v, 1000000)` |
| Force Index | `ta.force_index(close, volume)` | close, volume | Array | `fi = ta.force_index(close, volume)` |
| NVI | `ta.nvi(close, volume)` | close, volume | Array | `nvi = ta.nvi(close, volume)` |
| PVI | `ta.pvi(close, volume)` | close, volume | Array | `pvi = ta.pvi(close, volume)` |
| Volume Oscillator | `ta.volume_oscillator(v, fast, slow)` | volume, fast=5, slow=10 | Array (%) | `vo = ta.volume_oscillator(v, 5, 10)` |
| Volume ROC | `ta.vroc(volume, period)` | volume, period=25 | Array (%) | `vroc = ta.vroc(volume, 25)` |
| Klinger Volume Osc | `ta.kvo(h, l, c, v, fast=34, slow=55)` | 🔴 high, 🔴 low, 🔴 close, 🔴 volume, 🟢 fast=34, 🟢 slow=55 | Array | `kvo = ta.kvo(h, l, c, v)` |
| Price Volume Trend | `ta.pvt(close, volume)` | 🔴 close, 🔴 volume | Array | `pvt = ta.pvt(close, volume)` |

### 🔄 Oscillators (19)

| Indicator | Function | Parameters | Returns | Example |
|-----------|----------|------------|---------|---------|
| ROC | `ta.roc_oscillator(data, period)` | data, period=12 | Array (%) | `roc = ta.roc_oscillator(close, 12)` |
| CMO | `ta.cmo(data, period)` | data, period=14 | Array (-100 to 100) | `cmo = ta.cmo(close, 14)` |
| TRIX | `ta.trix(data, period)` | data, period=14 | Array | `trix = ta.trix(close, 14)` |
| Ultimate Oscillator | `ta.uo_oscillator(h, l, c, p1, p2, p3)` | high, low, close, p1=7, p2=14, p3=28 | Array | `uo = ta.uo_oscillator(h, l, c)` |
| Awesome Oscillator | `ta.awesome_oscillator(h, l, fast, slow)` | high, low, fast=5, slow=34 | Array | `ao = ta.awesome_oscillator(h, l)` |
| Accelerator Osc | `ta.accelerator_oscillator(h, l, period)` | high, low, period=5 | Array | `ac = ta.accelerator_oscillator(h, l)` |
| PPO | `ta.ppo(data, fast, slow, signal)` | data, fast=12, slow=26, signal=9 | (ppo, signal, hist) | `p, s, h = ta.ppo(close)` |
| Price Oscillator | `ta.price_oscillator(data, fast, slow, type)` | data, fast=10, slow=20, ma_type="SMA" | Array | `po = ta.price_oscillator(close)` |
| DPO | `ta.dpo(data, period)` | data, period=20 | Array | `dpo = ta.dpo(close, 20)` |
| Aroon Oscillator | `ta.aroon_oscillator(high, low, period)` | high, low, period=25 | Array (-100 to 100) | `ao = ta.aroon_oscillator(h, l, 25)` |
| Stochastic RSI | `ta.stochrsi(data, rsi=14, stoch=14, k=3, d=3)` | 🔴 data, 🟢 rsi=14, 🟢 stoch=14, 🟢 k=3, 🟢 d=3 | (k%, d%) | `k, d = ta.stochrsi(close)` |
| Relative Vigor Index | `ta.rvi(o, h, l, c, period=10)` | 🔴 open, 🔴 high, 🔴 low, 🔴 close, 🟢 period=10 | (rvi, signal) | `rvi, sig = ta.rvi(o, h, l, c)` |
| Chaikin Oscillator | `ta.cho(h, l, c, v, fast=3, slow=10)` | 🔴 high, 🔴 low, 🔴 close, 🔴 volume, 🟢 fast=3, 🟢 slow=10 | Array | `co = ta.cho(h, l, c, v)` |
| Choppiness Index | `ta.chop(high, low, close, period=14)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=14 | Array (0-100) | `chop = ta.chop(h, l, c)` |
| Know Sure Thing | `ta.kst(data, roc1=10, roc2=15, roc3=20, roc4=30, sma1=10, sma2=10, sma3=10, sma4=15, signal=9)` | 🔴 data, 🟢 ROC/SMA periods, 🟢 signal=9 | (kst, signal) | `kst, sig = ta.kst(close)` |
| Schaff Trend Cycle | `ta.stc(data, fast=23, slow=50, cycle=10, smooth1=3, smooth2=3)` | 🔴 data, 🟢 fast=23, 🟢 slow=50, 🟢 cycle=10, 🟢 smooth1=3, 🟢 smooth2=3 | Array (0-100) | `stc = ta.stc(close)` |
| True Strength Index | `ta.tsi(data, long=25, short=13, signal=13)` | 🔴 data, 🟢 long=25, 🟢 short=13, 🟢 signal=13 | (tsi, signal) | `tsi, sig = ta.tsi(close)` |
| Vortex Indicator | `ta.vortex(high, low, close, period=14)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=14 | (vi_plus, vi_minus) | `vip, vim = ta.vortex(h, l, c)` |
| Gator Oscillator | `ta.gator(data, jaw=13, teeth=8, lips=5)` | 🔴 data, 🟢 jaw=13, 🟢 teeth=8, 🟢 lips=5 | (upper, lower) | `u, l = ta.gator(hl2)` |

### 📐 Statistical Indicators (8)

| Indicator | Function | Parameters | Returns | Example |
|-----------|----------|------------|---------|---------|
| Linear Regression | `ta.linear_regression(data, period)` | data, period=14 | Array | `lr = ta.linear_regression(close, 14)` |
| LR Slope | `ta.linear_regression_slope(data, period)` | data, period=14 | Array | `slope = ta.linear_regression_slope(close, 14)` |
| Correlation | `ta.correlation(data1, data2, period)` | data1, data2, period=20 | Array (-1 to 1) | `corr = ta.correlation(stock1, stock2, 20)` |
| Beta | `ta.beta(asset, market, period)` | asset, market, period=252 | Array | `beta = ta.beta(stock, market, 252)` |
| Variance | `ta.variance(data, period)` | data, period=20 | Array | `var = ta.variance(close, 20)` |
| TSF | `ta.time_series_forecast(data, period)` | data, period=14 | Array | `tsf = ta.time_series_forecast(close, 14)` |
| Median | `ta.median(data, period)` | data, period=20 | Array | `med = ta.median(close, 20)` |
| Mode | `ta.mode(data, period, bins)` | data, period=20, bins=10 | Array | `mode = ta.mode(close, 20, 10)` |

### 🔀 Hybrid Indicators (10)

| Indicator | Function | Parameters | Returns | Example |
|-----------|----------|------------|---------|---------|
| ADX System | `ta.adx_system(h, l, c, period)` | high, low, close, period=14 | (+DI, -DI, ADX) | `p, m, adx = ta.adx_system(h, l, c, 14)` |
| Aroon System | `ta.aroon_system(high, low, period)` | high, low, period=25 | (up, down) | `up, down = ta.aroon_system(h, l, 25)` |
| Pivot Points | `ta.pivot_points(high, low, close)` | high, low, close | (P, R1, S1, R2, S2, R3, S3) | `p, r1, s1, r2, s2, r3, s3 = ta.pivot_points(h, l, c)` |
| Parabolic SAR | `ta.parabolic_sar(h, l, accel, max)` | high, low, accel=0.02, max=0.2 | (values, trend) | `sar, trend = ta.parabolic_sar(h, l)` |
| DMI | `ta.directional_movement(h, l, c, period)` | high, low, close, period=14 | (+DI, -DI) | `plus, minus = ta.directional_movement(h, l, c)` |
| PSAR | `ta.psar(high, low, accel, max)` | high, low, accel=0.02, max=0.2 | Array | `psar = ta.psar(h, l, 0.02, 0.2)` |
| Hilbert Trendline | `ta.hilbert_trendline(data)` | data | Array | `ht = ta.hilbert_trendline(close)` |
| Zig Zag | `ta.zigzag(high, low, close, deviation=5.0)` | 🔴 high, 🔴 low, 🔴 close, 🟢 deviation=5.0 | Array | `zz = ta.zigzag(h, l, c)` |
| Williams Fractals | `ta.fractals(high, low)` | 🔴 high, 🔴 low | (fractal_up, fractal_down) | `fu, fd = ta.fractals(h, l)` |
| Random Walk Index | `ta.rwi(high, low, close, period=14)` | 🔴 high, 🔴 low, 🔴 close, 🟢 period=14 | (rwi_high, rwi_low) | `rwh, rwl = ta.rwi(h, l, c)` |

### 🔧 Utility Functions (7)

| Function | Syntax | Parameters | Returns | Example |
|----------|--------|------------|---------|---------|
| Crossover | `ta.crossover(series1, series2)` | series1, series2 | Boolean array | `buy = ta.crossover(fast_ma, slow_ma)` |
| Crossunder | `ta.crossunder(series1, series2)` | series1, series2 | Boolean array | `sell = ta.crossunder(fast_ma, slow_ma)` |
| Highest | `ta.highest(data, period)` | data, period | Array | `hh = ta.highest(high, 20)` |
| Lowest | `ta.lowest(data, period)` | data, period | Array | `ll = ta.lowest(low, 20)` |
| Change | `ta.change(data, length)` | data, length=1 | Array | `chg = ta.change(close, 1)` |
| ROC | `ta.roc(data, length)` | data, length | Array (%) | `roc = ta.roc(close, 10)` |
| StdDev | `ta.stdev(data, period)` | data, period | Array | `std = ta.stdev(close, 20)` |

## Common Trading Patterns

### Moving Average Crossover
```python
# Golden Cross / Death Cross
ema_fast = ta.ema(close, 50)
ema_slow = ta.ema(close, 200)
golden_cross = ta.crossover(ema_fast, ema_slow)
death_cross = ta.crossunder(ema_fast, ema_slow)
```

### RSI Divergence
```python
# Bullish divergence: Price makes lower low, RSI makes higher low
rsi = ta.rsi(close, 14)
price_ll = close == ta.lowest(close, 20)
rsi_hl = rsi > ta.lowest(rsi, 20)
bullish_divergence = price_ll & rsi_hl
```

### Bollinger Band Squeeze
```python
# Volatility contraction
upper, middle, lower = ta.bbands(close, 20, 2)
bandwidth = (upper - lower) / middle
squeeze = bandwidth == ta.lowest(bandwidth, 20)
```

### MACD Signal
```python
# MACD crossover with trend filter
macd_line, signal_line, histogram = ta.macd(close, 12, 26, 9)
sma_200 = ta.sma(close, 200)

bullish_macd = ta.crossover(macd_line, signal_line) & (close > sma_200)
bearish_macd = ta.crossunder(macd_line, signal_line) & (close < sma_200)
```

### Supertrend Strategy
```python
# Trend following with Supertrend
supertrend, direction = ta.supertrend(high, low, close, 10, 3)
buy_signal = direction == -1  # Bullish
sell_signal = direction == 1   # Bearish
stop_loss = supertrend  # Use as trailing stop
```

### Volume Confirmation
```python
# Price breakout with volume
high_20 = ta.highest(high, 20)
breakout = high >= high_20
volume_surge = volume > ta.sma(volume, 20) * 1.5
confirmed_breakout = breakout & volume_surge
```

## Position Sizing

### ATR-Based Position Sizing
```python
def position_size_atr(capital, risk_percent, atr_value, atr_multiplier=2):
    risk_amount = capital * (risk_percent / 100)
    stop_distance = atr_value * atr_multiplier
    shares = risk_amount / stop_distance
    return int(shares)

# Example
atr = ta.atr(high, low, close, 14)
shares = position_size_atr(100000, 1, atr[-1], 2)
```

### Volatility-Adjusted Sizing
```python
def position_size_volatility(capital, base_risk, current_vol, avg_vol):
    adjusted_risk = base_risk * (avg_vol / current_vol)
    adjusted_risk = max(0.5, min(2.0, adjusted_risk))  # Cap between 0.5% and 2%
    return capital * (adjusted_risk / 100)

# Example
current_atr = ta.atr(high, low, close, 14)[-1]
avg_atr = ta.sma(ta.atr(high, low, close, 14), 50)[-1]
risk_amount = position_size_volatility(100000, 1, current_atr, avg_atr)
```

## Performance Tips

1. **Use NumPy arrays** for best performance
   ```python
   close_np = np.array(price_list)  # Convert once
   sma = ta.sma(close_np, 20)       # Fast calculation
   ```

2. **Batch calculations** to minimize overhead
   ```python
   # Calculate all at once
   indicators = {
       'sma_20': ta.sma(close, 20),
       'ema_20': ta.ema(close, 20),
       'rsi_14': ta.rsi(close, 14),
       'atr_14': ta.atr(high, low, close, 14)
   }
   ```

3. **Reuse calculations** when possible
   ```python
   # Calculate once, use multiple times
   atr_14 = ta.atr(high, low, close, 14)
   position_size = calculate_size(atr_14[-1])
   stop_loss = close[-1] - (2 * atr_14[-1])
   take_profit = close[-1] + (3 * atr_14[-1])
   ```

## Complete Strategy Template

```python
from openalgo import ta
import numpy as np

class TradingStrategy:
    def __init__(self, capital=100000, risk_percent=1):
        self.capital = capital
        self.risk_percent = risk_percent
        
    def analyze(self, high, low, close, volume):
        # Calculate all indicators
        indicators = self._calculate_indicators(high, low, close, volume)
        
        # Generate signal
        signal = self._generate_signal(indicators, close)
        
        # Risk management
        risk_params = self._calculate_risk(indicators, close)
        
        return {
            'signal': signal,
            'indicators': indicators,
            'risk': risk_params
        }
    
    def _calculate_indicators(self, high, low, close, volume):
        return {
            # Trend
            'sma_50': ta.sma(close, 50),
            'sma_200': ta.sma(close, 200),
            'ema_20': ta.ema(close, 20),
            'supertrend': ta.supertrend(high, low, close, 10, 3),
            
            # Momentum
            'rsi': ta.rsi(close, 14),
            'macd': ta.macd(close, 12, 26, 9),
            'stoch': ta.stochastic(high, low, close, 14, 3),
            
            # Volatility
            'atr': ta.atr(high, low, close, 14),
            'bbands': ta.bbands(close, 20, 2),
            
            # Volume
            'obv': ta.obv(close, volume),
            'cmf': ta.cmf(high, low, close, volume, 20),
            'mfi': ta.mfi(high, low, close, volume, 14)
        }
    
    def _generate_signal(self, indicators, close):
        # Extract latest values
        i = -1  # Latest index
        
        # Trend conditions
        trend_up = (
            close[i] > indicators['sma_200'][i] and
            indicators['sma_50'][i] > indicators['sma_200'][i]
        )
        
        # Momentum conditions
        rsi_ok = 30 < indicators['rsi'][i] < 70
        macd_bullish = indicators['macd'][0][i] > indicators['macd'][1][i]
        
        # Volume confirmation
        volume_positive = indicators['cmf'][i] > 0
        
        # Generate signal
        if trend_up and rsi_ok and macd_bullish and volume_positive:
            return "BUY"
        elif not trend_up and rsi_ok and not macd_bullish and not volume_positive:
            return "SELL"
        else:
            return "HOLD"
    
    def _calculate_risk(self, indicators, close):
        atr = indicators['atr'][-1]
        
        # Position sizing
        risk_amount = self.capital * (self.risk_percent / 100)
        stop_distance = atr * 2
        position_size = int(risk_amount / stop_distance)
        
        # Stop loss and take profit
        if indicators['supertrend'][1][-1] == -1:  # Bullish
            stop_loss = close[-1] - stop_distance
            take_profit = close[-1] + (stop_distance * 2)
        else:  # Bearish
            stop_loss = close[-1] + stop_distance
            take_profit = close[-1] - (stop_distance * 2)
        
        return {
            'position_size': position_size,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk_amount': risk_amount
        }

# Usage
strategy = TradingStrategy(capital=100000, risk_percent=1)
result = strategy.analyze(high, low, close, volume)
print(f"Signal: {result['signal']}")
print(f"Position: {result['risk']['position_size']} shares")
print(f"Stop: ${result['risk']['stop_loss']:.2f}")
print(f"Target: ${result['risk']['take_profit']:.2f}")
```

## ✨ New Indicators Added

### Advanced Momentum & Oscillators

```python
# Stochastic RSI - combines RSI with stochastic calculation
k, d = ta.stoch_rsi(close, rsi_period=14, stoch_period=14, k_period=3, d_period=3)

# Relative Vigor Index - measures price vigor relative to trading range
rvi, signal = ta.rvi(open_prices, high, low, close, period=10)

# Chaikin Oscillator - momentum of Accumulation/Distribution Line
chaikin_osc = ta.chaikin_osc(high, low, close, volume, fast_period=3, slow_period=10)

# Balance of Power - measures buyer vs seller strength
bop = ta.bop(open_prices, high, low, close)

# Elder Ray Index - bull and bear power
bull_power, bear_power = ta.elder_ray(high, low, close, period=13)

# Fisher Transform - converts prices to normal distribution
fisher, trigger = ta.fisher_transform((high + low) / 2, period=10)

# Connors RSI - composite momentum oscillator
connors_rsi = ta.connors_rsi(close, rsi_period=3, streak_period=2, roc_period=100)
```

### Advanced Volume Indicators

```python
# Klinger Volume Oscillator - predicts price reversals using volume
kvo = ta.kvo(high, low, close, volume, fast_period=34, slow_period=55)

# Price Volume Trend - cumulative volume based on price changes
pvt = ta.pvt(close, volume)
```

### Advanced Trend Indicators

```python
# Chande Kroll Stop - trailing stop-loss using ATR
long_stop, short_stop = ta.chande_kroll_stop(high, low, close, period=10, mult=1.0)

# Triangular Moving Average - double-smoothed average
trima = ta.trima(close, period=20)

# McGinley Dynamic - automatically adjusts for market speed
mcginley = ta.mcginley(close, period=14)

# VIDYA - uses CMO to adjust EMA smoothing
vidya = ta.vidya(close, period=14, alpha=0.2)

# Alligator - Bill Williams indicator with three SMMA lines
jaw, teeth, lips = ta.alligator((high + low) / 2)

# Moving Average Envelopes - percentage bands around MA
upper, middle, lower = ta.ma_envelopes(close, period=20, percentage=2.5, ma_type="SMA")
```

### Advanced Oscillators

```python
# Choppiness Index - measures trending vs ranging markets
chop = ta.chop(high, low, close, period=14)

# Know Sure Thing - smoothed rate-of-change momentum oscillator
kst, signal = ta.kst(close)

# Schaff Trend Cycle - combines MACD with stochastics
stc = ta.stc(close, fast=23, slow=50, cycle=10)

# True Strength Index - double-smoothed momentum oscillator
tsi, signal = ta.tsi(close, long=25, short=13)

# Vortex Indicator - identifies trend changes
vi_plus, vi_minus = ta.vortex(high, low, close, period=14)

# Gator Oscillator - shows Alligator convergence/divergence
upper, lower = ta.gator((high + low) / 2)
```

### Advanced Volatility Indicators

```python
# Bollinger Bands %B - position relative to bands
bb_percent_b = ta.bb_percent_b(close, period=20, std_dev=2.0)

# Bollinger Bandwidth - measures band width
bb_bandwidth = ta.bb_bandwidth(close, period=20, std_dev=2.0)

# Chandelier Exit - trailing stop based on highest/lowest
long_exit, short_exit = ta.chandelier_exit(high, low, close, period=22, multiplier=3.0)

# Historical Volatility - realized volatility measure
hv = ta.hv(close, period=20, annualize=True)

# Ulcer Index - downside risk measure
ui = ta.ulcer_index(close, period=14)

# STARC Bands - SMA with ATR-based bands
upper, middle, lower = ta.starc_bands(high, low, close, ma_period=20, atr_period=15, multiplier=2.0)
```

### Advanced Pattern Recognition

```python
# Zig Zag - connects significant price swings
zigzag = ta.zigzag(high, low, close, deviation=5.0)

# Williams Fractals - identifies reversal points
fractal_up, fractal_down = ta.fractals(high, low)

# Random Walk Index - measures trend strength
rwi_high, rwi_low = ta.rwi(high, low, close, period=14)
```

### Example Usage in Trading Strategy

```python
import numpy as np
from openalgo import ta

# Sample data
high = np.random.randn(100).cumsum() + 100
low = high - np.random.rand(100) * 2
close = low + (high - low) * np.random.rand(100)
open_prices = np.roll(close, 1)
volume = np.random.randint(1000, 10000, 100)

# Advanced momentum analysis
stoch_k, stoch_d = ta.stoch_rsi(close)
rvi_main, rvi_signal = ta.rvi(open_prices, high, low, close)
connors = ta.connors_rsi(close)

# Advanced volume analysis
kvo = ta.kvo(high, low, close, volume)
pvt = ta.pvt(close, volume)

# Risk management with Chande Kroll Stop
long_stop, short_stop = ta.chande_kroll_stop(high, low, close)

# Trading signals
buy_signal = (stoch_k[-1] > stoch_d[-1]) & (rvi_main[-1] > rvi_signal[-1]) & (kvo[-1] > 0)
sell_signal = (stoch_k[-1] < stoch_d[-1]) & (rvi_main[-1] < rvi_signal[-1]) & (kvo[-1] < 0)

print(f"Latest signals:")
print(f"Stochastic RSI: K={stoch_k[-1]:.2f}, D={stoch_d[-1]:.2f}")
print(f"RVI: {rvi_main[-1]:.4f}, Signal: {rvi_signal[-1]:.4f}")
print(f"Connors RSI: {connors[-1]:.2f}")
print(f"KVO: {kvo[-1]:.2f}")
print(f"Buy Signal: {buy_signal}, Sell Signal: {sell_signal}")
print(f"Stop Levels: Long={long_stop[-1]:.2f}, Short={short_stop[-1]:.2f}")
```