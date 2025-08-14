# OpenAlgo Technical Indicators - Parameters Reference

This document provides a comprehensive reference for all indicator function parameters, clearly distinguishing between **mandatory** and **optional** parameters with their default values.

## Parameter Legend

- 🔴 **MANDATORY** - Must be provided
- 🟢 **OPTIONAL** - Has default value, can be omitted
- 📊 **Data Types**: `Union[np.ndarray, pd.Series, list]`

---

## 📈 Trend Indicators

### Simple Moving Average (SMA)
```python
ta.sma(data, period)
```
- 🔴 **data**: Price data (typically close prices)
- 🔴 **period**: Number of periods for moving average

**Example:**
```python
sma_20 = ta.sma(close, 20)  # 20-period SMA
```

### Exponential Moving Average (EMA)
```python
ta.ema(data, period)
```
- 🔴 **data**: Price data
- 🔴 **period**: Number of periods for moving average

**Example:**
```python
ema_50 = ta.ema(close, 50)  # 50-period EMA
```

### Weighted Moving Average (WMA)
```python
ta.wma(data, period)
```
- 🔴 **data**: Price data
- 🔴 **period**: Number of periods for moving average

### Double Exponential Moving Average (DEMA)
```python
ta.dema(data, period)
```
- 🔴 **data**: Price data
- 🔴 **period**: Number of periods for moving average

### Triple Exponential Moving Average (TEMA)
```python
ta.tema(data, period)
```
- 🔴 **data**: Price data
- 🔴 **period**: Number of periods for moving average

### Hull Moving Average (HMA)
```python
ta.hma(data, period)
```
- 🔴 **data**: Price data
- 🔴 **period**: Number of periods for moving average

### Volume Weighted Moving Average (VWMA)
```python
ta.vwma(data, volume, period)
```
- 🔴 **data**: Price data
- 🔴 **volume**: Volume data
- 🔴 **period**: Number of periods for moving average

### Arnaud Legoux Moving Average (ALMA)
```python
ta.alma(data, period=21, offset=0.85, sigma=6.0)
```
- 🔴 **data**: Price data
- 🟢 **period**: Lookback period (default: **21**)
- 🟢 **offset**: Gaussian offset (default: **0.85**)
- 🟢 **sigma**: Standard deviation (default: **6.0**)

**Example:**
```python
alma_default = ta.alma(close)                    # Uses defaults
alma_custom = ta.alma(close, 30, 0.9, 7.0)     # Custom parameters
```

### Kaufman's Adaptive Moving Average (KAMA)
```python
ta.kama(data, period=10, fast_period=2, slow_period=30)
```
- 🔴 **data**: Price data
- 🟢 **period**: Efficiency ratio period (default: **10**)
- 🟢 **fast_period**: Fast EMA period (default: **2**)
- 🟢 **slow_period**: Slow EMA period (default: **30**)

**Example:**
```python
kama_default = ta.kama(close)                   # Uses defaults
kama_custom = ta.kama(close, 14, 3, 40)        # Custom parameters
```

### Zero Lag Exponential Moving Average (ZLEMA)
```python
ta.zlema(data, period)
```
- 🔴 **data**: Price data
- 🔴 **period**: Number of periods for moving average

### T3 Moving Average
```python
ta.t3(data, period=21, v_factor=0.7)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **21**)
- 🟢 **v_factor**: Volume factor (default: **0.7**)

**Example:**
```python
t3_default = ta.t3(close)                       # Uses defaults
t3_custom = ta.t3(close, 30, 0.8)              # Custom parameters
```

### Fractal Adaptive Moving Average (FRAMA)
```python
ta.frama(data, period=16)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **16**)

**Example:**
```python
frama_default = ta.frama(close)                 # Uses period=16
frama_custom = ta.frama(close, 20)             # Custom period
```

### Supertrend
```python
ta.supertrend(high, low, close, period=10, multiplier=3.0)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: ATR period (default: **10**)
- 🟢 **multiplier**: ATR multiplier (default: **3.0**)

**Example:**
```python
st_default, dir_default = ta.supertrend(high, low, close)      # Uses defaults
st_custom, dir_custom = ta.supertrend(high, low, close, 14, 2.5)  # Custom
```

### Ichimoku Cloud
```python
ta.ichimoku(high, low, close, tenkan_period=9, kijun_period=26, 
           senkou_b_period=52, displacement=26)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **tenkan_period**: Conversion line period (default: **9**)
- 🟢 **kijun_period**: Base line period (default: **26**)
- 🟢 **senkou_b_period**: Leading span B period (default: **52**)
- 🟢 **displacement**: Cloud displacement (default: **26**)

**Example:**
```python
# Uses default Ichimoku settings
tenkan, kijun, span_a, span_b, chikou = ta.ichimoku(high, low, close)

# Custom settings
tenkan, kijun, span_a, span_b, chikou = ta.ichimoku(high, low, close, 7, 22, 44, 22)
```

### Triangular Moving Average (TRIMA)
```python
ta.trima(data, period)
```
- 🔴 **data**: Price data
- 🔴 **period**: Number of periods for moving average

### McGinley Dynamic
```python
ta.mcginley_dynamic(data, period=14)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: 14)

### VIDYA (Variable Index Dynamic Average)
```python
ta.vidya(data, period=14, alpha=0.2)
```
- 🔴 **data**: Price data
- 🟢 **period**: CMO calculation period (default: 14)
- 🟢 **alpha**: EMA smoothing factor (default: 0.2)

### Alligator (Bill Williams)
```python
ta.alligator(high, low, jaw_period=13, jaw_shift=8, teeth_period=8, teeth_shift=5, lips_period=5, lips_shift=3)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **jaw_period**: Jaw (blue line) period (default: 13)
- 🟢 **jaw_shift**: Jaw shift forward (default: 8)
- 🟢 **teeth_period**: Teeth (red line) period (default: 8)
- 🟢 **teeth_shift**: Teeth shift forward (default: 5)
- 🟢 **lips_period**: Lips (green line) period (default: 5)
- 🟢 **lips_shift**: Lips shift forward (default: 3)

**Returns:** Tuple of (jaw, teeth, lips)

### Moving Average Envelopes
```python
ta.ma_envelopes(data, period=20, percentage=2.5, ma_type='SMA')
```
- 🔴 **data**: Price data
- 🟢 **period**: Moving average period (default: 20)
- 🟢 **percentage**: Envelope percentage (default: 2.5)
- 🟢 **ma_type**: MA type 'SMA' or 'EMA' (default: 'SMA')

**Returns:** Tuple of (upper_envelope, ma_line, lower_envelope)

### Chande Kroll Stop
```python
ta.ckstop(high, low, close, period=10, atr_multiplier=1.0)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: ATR period (default: 10)
- 🟢 **atr_multiplier**: ATR multiplier (default: 1.0)

**Returns:** Tuple of (Long Stop, Short Stop)

---

## 💫 Momentum Indicators

### Relative Strength Index (RSI)
```python
ta.rsi(data, period=14)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **14**)

**Example:**
```python
rsi_default = ta.rsi(close)                     # Uses period=14
rsi_custom = ta.rsi(close, 21)                 # Custom period
```

### Moving Average Convergence Divergence (MACD)
```python
ta.macd(data, fast_period=12, slow_period=26, signal_period=9)
```
- 🔴 **data**: Price data
- 🟢 **fast_period**: Fast EMA period (default: **12**)
- 🟢 **slow_period**: Slow EMA period (default: **26**)
- 🟢 **signal_period**: Signal line EMA period (default: **9**)

**Example:**
```python
macd, signal, hist = ta.macd(close)                    # Uses defaults
macd, signal, hist = ta.macd(close, 10, 20, 7)        # Custom parameters
```

### Stochastic Oscillator
```python
ta.stochastic(high, low, close, k_period=14, d_period=3)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **k_period**: %K calculation period (default: **14**)
- 🟢 **d_period**: %D calculation period (default: **3**)

**Example:**
```python
k, d = ta.stochastic(high, low, close)                 # Uses defaults
k, d = ta.stochastic(high, low, close, 21, 5)         # Custom parameters
```

### Commodity Channel Index (CCI)
```python
ta.cci(high, low, close, period=20)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: **20**)

**Example:**
```python
cci_default = ta.cci(high, low, close)                 # Uses period=20
cci_custom = ta.cci(high, low, close, 14)             # Custom period
```

### Williams %R
```python
ta.williams_r(high, low, close, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: **14**)

**Example:**
```python
wr_default = ta.williams_r(high, low, close)           # Uses period=14
wr_custom = ta.williams_r(high, low, close, 21)       # Custom period
```

### Balance of Power (BOP)
```python
ta.bop(open, high, low, close)
```
- 🔴 **open**: Open prices
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices

### Elder Ray Index
```python
ta.elderray(high, low, close, period=13)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: EMA period (default: 13)

**Returns:** Tuple of (Bull Power, Bear Power)

### Fisher Transform
```python
ta.fisher(data, period=10)
```
- 🔴 **data**: Price data
- 🟢 **period**: Smoothing period (default: 10)

**Returns:** Tuple of (Fisher Transform, Trigger line)

### Connors RSI
```python
ta.crsi(data, rsi_period=3, streak_period=2, roc_period=100)
```
- 🔴 **data**: Close prices
- 🟢 **rsi_period**: RSI period (default: 3)
- 🟢 **streak_period**: Streak period (default: 2)
- 🟢 **roc_period**: ROC period (default: 100)

### Choppiness Index (CHOP)
```python
ta.chop(high, low, close, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: 14)

### Know Sure Thing (KST)
```python
ta.kst(close, roc1=10, roc2=15, roc3=20, roc4=30, sma1=10, sma2=10, sma3=10, sma4=15, signal_period=9)
```
- 🔴 **close**: Close prices
- 🟢 **roc1**: First ROC period (default: 10)
- 🟢 **roc2**: Second ROC period (default: 15)
- 🟢 **roc3**: Third ROC period (default: 20)
- 🟢 **roc4**: Fourth ROC period (default: 30)
- 🟢 **sma1**: First SMA period (default: 10)
- 🟢 **sma2**: Second SMA period (default: 10)
- 🟢 **sma3**: Third SMA period (default: 10)
- 🟢 **sma4**: Fourth SMA period (default: 15)
- 🟢 **signal_period**: Signal line SMA period (default: 9)

**Returns:** Tuple of (KST line, Signal line)

### True Strength Index (TSI)
```python
ta.tsi(close, long_period=25, short_period=13, signal_period=13)
```
- 🔴 **close**: Close prices
- 🟢 **long_period**: First smoothing period (default: 25)
- 🟢 **short_period**: Second smoothing period (default: 13)
- 🟢 **signal_period**: Signal line EMA period (default: 13)

**Returns:** Tuple of (TSI line, Signal line)

### Vortex Indicator (VI)
```python
ta.vi(high, low, close, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: 14)

**Returns:** Tuple of (VI+, VI-)

### Schaff Trend Cycle (STC)
```python
ta.stc(close, fast_period=23, slow_period=50, cycle_period=10, d1_period=3, d2_period=3)
```
- 🔴 **close**: Close prices
- 🟢 **fast_period**: Fast EMA period (default: 23)
- 🟢 **slow_period**: Slow EMA period (default: 50)
- 🟢 **cycle_period**: Stochastic period (default: 10)
- 🟢 **d1_period**: First %K smoothing (default: 3)
- 🟢 **d2_period**: Second %K smoothing (default: 3)

### Gator Oscillator
```python
ta.gator_oscillator(high, low, jaw_period=13, jaw_shift=8, teeth_period=8, teeth_shift=5, lips_period=5, lips_shift=3)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **jaw_period**: Jaw (blue line) period (default: 13)
- 🟢 **jaw_shift**: Jaw shift forward (default: 8)
- 🟢 **teeth_period**: Teeth (red line) period (default: 8)
- 🟢 **teeth_shift**: Teeth shift forward (default: 5)
- 🟢 **lips_period**: Lips (green line) period (default: 5)
- 🟢 **lips_shift**: Lips shift forward (default: 3)

**Returns:** Tuple of (Upper Gator, Lower Gator)

### Stochastic RSI
```python
ta.stochrsi(data, rsi_period=14, stoch_period=14, k_period=3, d_period=3)
```
- 🔴 **data**: Close prices
- 🟢 **rsi_period**: RSI calculation period (default: 14)
- 🟢 **stoch_period**: Stochastic period (default: 14)
- 🟢 **k_period**: %K smoothing period (default: 3)
- 🟢 **d_period**: %D smoothing period (default: 3)

**Returns:** Tuple of (StochRSI %K, StochRSI %D)

### Relative Vigor Index (RVI)
```python
ta.rvi(open, high, low, close, period=10)
```
- 🔴 **open**: Open prices
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: 10)

**Returns:** Tuple of (RVI line, Signal line)

### Chaikin Oscillator
```python
ta.cho(high, low, close, volume, fast_period=3, slow_period=10)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data
- 🟢 **fast_period**: Fast EMA period (default: 3)
- 🟢 **slow_period**: Slow EMA period (default: 10)

---

## 📊 Volatility Indicators

### Average True Range (ATR)
```python
ta.atr(high, low, close, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: **14**)

**Example:**
```python
atr_default = ta.atr(high, low, close)                 # Uses period=14
atr_custom = ta.atr(high, low, close, 20)             # Custom period
```

### Bollinger Bands
```python
ta.bbands(data, period=20, std_dev=2.0)
```
- 🔴 **data**: Price data
- 🟢 **period**: Moving average period (default: **20**)
- 🟢 **std_dev**: Standard deviation multiplier (default: **2.0**)

**Example:**
```python
upper, middle, lower = ta.bbands(close)                # Uses defaults (20, 2.0)
upper, middle, lower = ta.bbands(close, 14, 1.5)      # Custom parameters
```

### Keltner Channel
```python
ta.keltner_channel(high, low, close, ema_period=20, atr_period=10, multiplier=2.0)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **ema_period**: EMA period (default: **20**)
- 🟢 **atr_period**: ATR period (default: **10**)
- 🟢 **multiplier**: ATR multiplier (default: **2.0**)

**Example:**
```python
upper, middle, lower = ta.keltner_channel(high, low, close)           # Uses defaults
upper, middle, lower = ta.keltner_channel(high, low, close, 14, 14, 1.5)  # Custom
```

### Donchian Channel
```python
ta.donchian_channel(high, low, period=20)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **period**: Number of periods (default: **20**)

**Example:**
```python
upper, middle, lower = ta.donchian_channel(high, low)         # Uses period=20
upper, middle, lower = ta.donchian_channel(high, low, 14)    # Custom period
```

### Chaikin Volatility
```python
ta.chaikin_volatility(high, low, ema_period=10, roc_period=10)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **ema_period**: EMA period (default: **10**)
- 🟢 **roc_period**: ROC period (default: **10**)

### Normalized Average True Range (NATR)
```python
ta.natr(high, low, close, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: **14**)

### Relative Volatility Index (RVI)
```python
ta.rvi_volatility(data, stdev_period=10, rsi_period=14)
```
- 🔴 **data**: Price data
- 🟢 **stdev_period**: Standard deviation period (default: **10**)
- 🟢 **rsi_period**: RSI calculation period (default: **14**)

### Ultimate Oscillator
```python
ta.ultimate_oscillator(high, low, close, period1=7, period2=14, period3=28)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period1**: First period (default: **7**)
- 🟢 **period2**: Second period (default: **14**)
- 🟢 **period3**: Third period (default: **28**)

### Standard Deviation
```python
ta.stddev(data, period=20)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **20**)

### True Range
```python
ta.true_range(high, low, close)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices

### Mass Index
```python
ta.mass_index(high, low, fast_period=9, slow_period=25)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **fast_period**: Fast EMA period (default: **9**)
- 🟢 **slow_period**: Sum period (default: **25**)

### Bollinger Bands %B
```python
ta.bbands_percent_b(close, period=20, std_dev=2)
```
- 🔴 **close**: Close prices
- 🟢 **period**: MA period (default: 20)
- 🟢 **std_dev**: Standard deviations (default: 2)

### Bollinger Bandwidth
```python
ta.bbands_bandwidth(close, period=20, std_dev=2)
```
- 🔴 **close**: Close prices
- 🟢 **period**: MA period (default: 20)
- 🟢 **std_dev**: Standard deviations (default: 2)

### Chandelier Exit
```python
ta.chandelier_exit(high, low, close, period=22, multiplier=3.0)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: ATR period (default: 22)
- 🟢 **multiplier**: ATR multiplier (default: 3.0)

**Returns:** Tuple of (Chandelier Exit Long, Chandelier Exit Short)

### Historical Volatility (HV)
```python
ta.hv(close, period=20, annualize=True)
```
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: 20)
- 🟢 **annualize**: Annualize result (default: True)

### Ulcer Index
```python
ta.ulcer_index(close, period=14)
```
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: 14)

### STARC Bands
```python
ta.starc_bands(high, low, close, ma_period=20, atr_period=15, multiplier=2.0)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **ma_period**: Moving average period (default: 20)
- 🟢 **atr_period**: ATR period (default: 15)
- 🟢 **multiplier**: ATR multiplier (default: 2.0)

**Returns:** Tuple of (Upper STARC, Middle STARC, Lower STARC)

---

## 📉 Volume Indicators

### On Balance Volume (OBV)
```python
ta.obv(close, volume)
```
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data

### Volume Weighted Average Price (VWAP)
```python
ta.vwap(high, low, close, volume, period=0)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data
- 🟢 **period**: Period for rolling VWAP, 0 for cumulative (default: **0**)

**Example:**
```python
vwap_cumulative = ta.vwap(high, low, close, volume)        # Cumulative VWAP
vwap_rolling = ta.vwap(high, low, close, volume, 20)       # 20-period rolling VWAP
```

### Money Flow Index (MFI)
```python
ta.mfi(high, low, close, volume, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data
- 🟢 **period**: Number of periods (default: **14**)

**Example:**
```python
mfi_default = ta.mfi(high, low, close, volume)             # Uses period=14
mfi_custom = ta.mfi(high, low, close, volume, 21)         # Custom period
```

### Accumulation/Distribution Line (ADL)
```python
ta.adl(high, low, close, volume)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data

### Chaikin Money Flow (CMF)
```python
ta.cmf(high, low, close, volume, period=20)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data
- 🟢 **period**: Number of periods (default: **20**)

### Ease of Movement (EMV)
```python
ta.emv(high, low, volume, scale=1000000)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **volume**: Volume data
- 🟢 **scale**: Scale factor (default: **1000000**)

### Force Index
```python
ta.force_index(close, volume)
```
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data

### Negative Volume Index (NVI)
```python
ta.nvi(close, volume)
```
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data

### Positive Volume Index (PVI)
```python
ta.pvi(close, volume)
```
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data

### Volume Oscillator
```python
ta.volume_oscillator(volume, fast_period=5, slow_period=10)
```
- 🔴 **volume**: Volume data
- 🟢 **fast_period**: Fast MA period (default: **5**)
- 🟢 **slow_period**: Slow MA period (default: **10**)

### Volume Rate of Change (VROC)
```python
ta.vroc(volume, period=25)
```
- 🔴 **volume**: Volume data
- 🟢 **period**: Number of periods (default: **25**)

### Klinger Volume Oscillator (KVO)
```python
ta.kvo(high, low, close, volume, fast_period=34, slow_period=55)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data
- 🟢 **fast_period**: Fast EMA period (default: 34)
- 🟢 **slow_period**: Slow EMA period (default: 55)

### Price Volume Trend (PVT)
```python
ta.pvt(close, volume)
```
- 🔴 **close**: Close prices
- 🔴 **volume**: Volume data

---

## 🔄 Oscillators

### Rate of Change (ROC)
```python
ta.roc_oscillator(data, period=12)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **12**)

### Chande Momentum Oscillator (CMO)
```python
ta.cmo(data, period=14)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **14**)

### TRIX
```python
ta.trix(data, period=14)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **14**)

### Ultimate Oscillator
```python
ta.uo_oscillator(high, low, close, period1=7, period2=14, period3=28)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period1**: First period (default: **7**)
- 🟢 **period2**: Second period (default: **14**)
- 🟢 **period3**: Third period (default: **28**)

### Awesome Oscillator
```python
ta.awesome_oscillator(high, low, fast_period=5, slow_period=34)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **fast_period**: Fast SMA period (default: **5**)
- 🟢 **slow_period**: Slow SMA period (default: **34**)

### Accelerator Oscillator
```python
ta.accelerator_oscillator(high, low, period=5)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **period**: SMA period for AO smoothing (default: **5**)

### Percentage Price Oscillator (PPO)
```python
ta.ppo(data, fast_period=12, slow_period=26, signal_period=9)
```
- 🔴 **data**: Price data
- 🟢 **fast_period**: Fast EMA period (default: **12**)
- 🟢 **slow_period**: Slow EMA period (default: **26**)
- 🟢 **signal_period**: Signal line period (default: **9**)

### Price Oscillator
```python
ta.price_oscillator(data, fast_period=10, slow_period=20, ma_type="SMA")
```
- 🔴 **data**: Price data
- 🟢 **fast_period**: Fast MA period (default: **10**)
- 🟢 **slow_period**: Slow MA period (default: **20**)
- 🟢 **ma_type**: Moving average type (default: **"SMA"**)

### Detrended Price Oscillator (DPO)
```python
ta.dpo(data, period=20)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **20**)

### Aroon Oscillator
```python
ta.aroon_oscillator(high, low, period=25)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **period**: Number of periods (default: **25**)

---

## 📐 Statistical Indicators

### Linear Regression
```python
ta.linear_regression(data, period=14)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **14**)

### Linear Regression Slope
```python
ta.linear_regression_slope(data, period=14)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **14**)

### Pearson Correlation Coefficient
```python
ta.correlation(data1, data2, period=20)
```
- 🔴 **data1**: First dataset
- 🔴 **data2**: Second dataset
- 🟢 **period**: Number of periods (default: **20**)

### Beta Coefficient
```python
ta.beta(asset, market, period=252)
```
- 🔴 **asset**: Asset price data
- 🔴 **market**: Market price data
- 🟢 **period**: Number of periods, typically 1 year (default: **252**)

### Variance
```python
ta.variance(data, period=20)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **20**)

### Time Series Forecast (TSF)
```python
ta.time_series_forecast(data, period=14)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **14**)

### Rolling Median
```python
ta.median(data, period=20)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **20**)

### Rolling Mode
```python
ta.mode(data, period=20, bins=10)
```
- 🔴 **data**: Price data
- 🟢 **period**: Number of periods (default: **20**)
- 🟢 **bins**: Number of bins for discretization (default: **10**)

---

## 🔀 Hybrid Indicators

### Average Directional Index (ADX) System
```python
ta.adx_system(high, low, close, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: **14**)

### Aroon System
```python
ta.aroon_system(high, low, period=25)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **period**: Number of periods (default: **25**)

### Pivot Points
```python
ta.pivot_points(high, low, close)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices

### Parabolic SAR
```python
ta.parabolic_sar(high, low, acceleration=0.02, maximum=0.2)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **acceleration**: Acceleration factor (default: **0.02**)
- 🟢 **maximum**: Maximum acceleration (default: **0.2**)

### Directional Movement Index (DMI)
```python
ta.directional_movement(high, low, close, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: **14**)

### PSAR (values only)
```python
ta.psar(high, low, acceleration=0.02, maximum=0.2)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **acceleration**: Acceleration factor (default: **0.02**)
- 🟢 **maximum**: Maximum acceleration (default: **0.2**)

### Hilbert Transform Trendline
```python
ta.hilbert_trendline(data)
```
- 🔴 **data**: Price data

### Zig Zag
```python
ta.zigzag(high, low, deviation=5.0)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **deviation**: Minimum percentage change (default: 5.0)

### Williams Fractals
```python
ta.williams_fractals(high, low, period=2)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🟢 **period**: Number of periods (default: 2)

**Returns:** Tuple of (Fractal High, Fractal Low)

### Random Walk Index (RWI)
```python
ta.random_walk_index(high, low, close, period=14)
```
- 🔴 **high**: High prices
- 🔴 **low**: Low prices
- 🔴 **close**: Close prices
- 🟢 **period**: Number of periods (default: 14)

**Returns:** Tuple of (RWI High, RWI Low)

---

## 🔧 Utility Functions

### Crossover Detection
```python
ta.crossover(series1, series2)
```
- 🔴 **series1**: First data series
- 🔴 **series2**: Second data series

### Crossunder Detection
```python
ta.crossunder(series1, series2)
```
- 🔴 **series1**: First data series
- 🔴 **series2**: Second data series

### Highest Value
```python
ta.highest(data, period)
```
- 🔴 **data**: Input data
- 🔴 **period**: Window size

### Lowest Value
```python
ta.lowest(data, period)
```
- 🔴 **data**: Input data
- 🔴 **period**: Window size

### Change
```python
ta.change(data, length=1)
```
- 🔴 **data**: Input data
- 🟢 **length**: Number of periods to look back (default: **1**)

### Rate of Change
```python
ta.roc(data, length)
```
- 🔴 **data**: Input data
- 🔴 **length**: Number of periods to look back

### Standard Deviation
```python
ta.stdev(data, period)
```
- 🔴 **data**: Input data
- 🔴 **period**: Window size

---

## 📋 Quick Usage Examples

### Using Default Parameters
```python
from openalgo import ta
import numpy as np

# Sample data
close = np.array([100, 102, 101, 103, 104, 102, 105, 106, 104, 107])
high = close + 1
low = close - 1
volume = np.array([50000, 60000, 45000, 70000, 80000, 55000, 65000, 72000, 68000, 75000])

# Using default parameters (most common usage)
rsi = ta.rsi(close)                              # period=14 (default)
macd_line, signal, hist = ta.macd(close)        # 12, 26, 9 (defaults)
atr = ta.atr(high, low, close)                  # period=14 (default)
bb_upper, bb_mid, bb_lower = ta.bbands(close)   # period=20, std=2.0 (defaults)
```

### Using Custom Parameters
```python
# Custom parameters when defaults don't fit your needs
rsi_21 = ta.rsi(close, 21)                              # Custom period
macd_line, signal, hist = ta.macd(close, 10, 20, 7)    # Custom MACD settings
atr_20 = ta.atr(high, low, close, 20)                   # Custom ATR period
bb_upper, bb_mid, bb_lower = ta.bbands(close, 14, 1.5) # Custom Bollinger settings
```

### Mixed Usage
```python
# Mix of default and custom parameters
supertrend_vals, direction = ta.supertrend(high, low, close)           # Uses defaults (10, 3.0)
supertrend_tight, direction = ta.supertrend(high, low, close, 7, 2.0)  # Tighter settings

# Ichimoku with default settings
tenkan, kijun, span_a, span_b, chikou = ta.ichimoku(high, low, close)

# ALMA with custom offset but default period and sigma
alma_custom = ta.alma(close, offset=0.9)  # period=21, sigma=6.0 use defaults
```

---

## 💡 Parameter Selection Tips

### Trend Indicators
- **Shorter periods** (5-20) = More responsive, more signals
- **Longer periods** (50-200) = Smoother, fewer false signals
- **Common periods**: 20, 50, 100, 200

### Momentum Indicators
- **RSI**: 14 is standard, 21 for less sensitive
- **MACD**: 12/26/9 is classic, try 5/35/5 for different markets
- **Stochastic**: 14/3 is standard, 5/3 for faster signals

### Volatility Indicators
- **ATR**: 14 is standard, 20-30 for smoother
- **Bollinger Bands**: 20/2.0 is classic, try 20/1.5 for tighter bands
- **Standard deviations**: 2.0 captures ~95% of price action

### Volume Indicators
- **Volume periods**: Often use 10-20 for short-term, 50+ for long-term
- **MFI**: 14 is standard, similar to RSI

### Time Horizons
- **Scalping**: 5-15 periods
- **Day Trading**: 10-50 periods  
- **Swing Trading**: 20-100 periods
- **Position Trading**: 50-200 periods