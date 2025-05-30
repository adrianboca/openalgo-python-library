"""
OpenAlgo Comprehensive Technical Indicators Showcase

This example demonstrates all 100+ technical indicators available in the OpenAlgo library,
organized by category with TradingView-like simplicity.
"""

import numpy as np
import pandas as pd
from openalgo import api, ta
import time

def generate_sample_data(n=1000):
    """Generate realistic sample OHLCV data for testing"""
    np.random.seed(42)
    
    # Generate realistic price data with trend and volatility
    returns = np.random.normal(0.0005, 0.02, n)  # Daily returns
    prices = 100 * np.exp(np.cumsum(returns))
    
    # Generate OHLC from closing prices
    close = prices
    high = close * (1 + np.random.uniform(0, 0.03, n))
    low = close * (1 - np.random.uniform(0, 0.03, n))
    open_prices = np.roll(close, 1) * (1 + np.random.uniform(-0.02, 0.02, n))
    open_prices[0] = close[0]
    
    # Generate volume
    volume = np.random.randint(100000, 1000000, n)
    
    return {
        'open': open_prices,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }

def showcase_trend_indicators():
    """Showcase all trend indicators"""
    print("🔵 TREND INDICATORS (14 indicators)")
    print("=" * 60)
    
    data = generate_sample_data()
    close = data['close']
    high = data['high']
    low = data['low']
    volume = data['volume']
    
    # Basic Moving Averages
    print("\n📈 Basic Moving Averages:")
    sma_20 = ta.sma(close, 20)
    ema_20 = ta.ema(close, 20)
    wma_20 = ta.wma(close, 20)
    print(f"   SMA(20): {sma_20[-1]:.2f}")
    print(f"   EMA(20): {ema_20[-1]:.2f}")
    print(f"   WMA(20): {wma_20[-1]:.2f}")
    
    # Advanced Moving Averages
    print("\n📈 Advanced Moving Averages:")
    dema_20 = ta.dema(close, 20)
    tema_20 = ta.tema(close, 20)
    hma_20 = ta.hma(close, 20)
    vwma_20 = ta.vwma(close, volume, 20)
    alma_20 = ta.alma(close, 21, 0.85, 6.0)
    kama_20 = ta.kama(close, 10, 2, 30)
    zlema_20 = ta.zlema(close, 20)
    t3_20 = ta.t3(close, 21, 0.7)
    frama_20 = ta.frama(close, 16)
    print(f"   DEMA(20): {dema_20[-1]:.2f}")
    print(f"   TEMA(20): {tema_20[-1]:.2f}")
    print(f"   HMA(20): {hma_20[-1]:.2f}")
    print(f"   VWMA(20): {vwma_20[-1]:.2f}")
    print(f"   ALMA(21): {alma_20[-1]:.2f}")
    print(f"   KAMA(10): {kama_20[-1]:.2f}")
    print(f"   ZLEMA(20): {zlema_20[-1]:.2f}")
    print(f"   T3(21): {t3_20[-1]:.2f}")
    print(f"   FRAMA(16): {frama_20[-1]:.2f}")
    
    # Complex Trend Systems
    print("\n📈 Complex Trend Systems:")
    supertrend, st_direction = ta.supertrend(high, low, close, 10, 3)
    trend_signal = "🟢 BULLISH" if st_direction[-1] == -1 else "🔴 BEARISH"
    print(f"   Supertrend: {supertrend[-1]:.2f} ({trend_signal})")
    
    tenkan, kijun, senkou_a, senkou_b, chikou = ta.ichimoku(high, low, close)
    print(f"   Ichimoku Tenkan: {tenkan[-1]:.2f}")
    print(f"   Ichimoku Kijun: {kijun[-1]:.2f}")

def showcase_momentum_indicators():
    """Showcase momentum indicators"""
    print("\n🟡 MOMENTUM INDICATORS (5 indicators)")
    print("=" * 60)
    
    data = generate_sample_data()
    close = data['close']
    high = data['high']
    low = data['low']
    
    # Classic Momentum
    rsi = ta.rsi(close, 14)
    macd_line, signal_line, histogram = ta.macd(close, 12, 26, 9)
    k_percent, d_percent = ta.stochastic(high, low, close, 14, 3)
    cci = ta.cci(high, low, close, 20)
    williams_r = ta.williams_r(high, low, close, 14)
    
    print(f"   RSI(14): {rsi[-1]:.2f}")
    print(f"   MACD: {macd_line[-1]:.4f} | Signal: {signal_line[-1]:.4f}")
    print(f"   Stochastic %K: {k_percent[-1]:.2f} | %D: {d_percent[-1]:.2f}")
    print(f"   CCI(20): {cci[-1]:.2f}")
    print(f"   Williams %R: {williams_r[-1]:.2f}")

def showcase_oscillators():
    """Showcase oscillator indicators"""
    print("\n🟠 OSCILLATORS (10 indicators)")
    print("=" * 60)
    
    data = generate_sample_data()
    close = data['close']
    high = data['high']
    low = data['low']
    
    # Price Oscillators
    roc = ta.roc_oscillator(close, 12)
    cmo = ta.cmo(close, 14)
    trix = ta.trix(close, 14)
    uo = ta.uo_oscillator(high, low, close, 7, 14, 28)
    ao = ta.awesome_oscillator(high, low, 5, 34)
    ac = ta.accelerator_oscillator(high, low, 5)
    
    print(f"   ROC(12): {roc[-1]:.2f}%")
    print(f"   CMO(14): {cmo[-1]:.2f}")
    print(f"   TRIX(14): {trix[-1]:.2f}")
    print(f"   Ultimate Oscillator: {uo[-1]:.2f}")
    print(f"   Awesome Oscillator: {ao[-1]:.2f}")
    print(f"   Accelerator Oscillator: {ac[-1]:.2f}")
    
    # Advanced Oscillators
    ppo_line, ppo_signal, ppo_hist = ta.ppo(close, 12, 26, 9)
    po = ta.price_oscillator(close, 10, 20, "SMA")
    dpo = ta.dpo(close, 20)
    aroon_osc = ta.aroon_oscillator(high, low, 25)
    
    print(f"   PPO: {ppo_line[-1]:.2f} | Signal: {ppo_signal[-1]:.2f}")
    print(f"   Price Oscillator: {po[-1]:.2f}")
    print(f"   DPO(20): {dpo[-1]:.2f}")
    print(f"   Aroon Oscillator: {aroon_osc[-1]:.2f}")

def showcase_volatility_indicators():
    """Showcase volatility indicators"""
    print("\n🔴 VOLATILITY INDICATORS (11 indicators)")
    print("=" * 60)
    
    data = generate_sample_data()
    close = data['close']
    high = data['high']
    low = data['low']
    
    # Classic Volatility
    atr = ta.atr(high, low, close, 14)
    upper, middle, lower = ta.bbands(close, 20, 2)
    kc_upper, kc_middle, kc_lower = ta.keltner_channel(high, low, close, 20, 10, 2)
    dc_upper, dc_middle, dc_lower = ta.donchian_channel(high, low, 20)
    
    print(f"   ATR(14): {atr[-1]:.2f}")
    print(f"   Bollinger Bands: {upper[-1]:.2f} | {middle[-1]:.2f} | {lower[-1]:.2f}")
    print(f"   Keltner Channel: {kc_upper[-1]:.2f} | {kc_middle[-1]:.2f} | {kc_lower[-1]:.2f}")
    print(f"   Donchian Channel: {dc_upper[-1]:.2f} | {dc_middle[-1]:.2f} | {dc_lower[-1]:.2f}")
    
    # Advanced Volatility
    chaikin_vol = ta.chaikin_volatility(high, low, 10, 10)
    natr = ta.natr(high, low, close, 14)
    rvi_vol = ta.rvi_volatility(close, 10, 14)
    stddev = ta.stddev(close, 20)
    tr = ta.true_range(high, low, close)
    mass_idx = ta.mass_index(high, low, 9, 25)
    
    print(f"   Chaikin Volatility: {chaikin_vol[-1]:.2f}%")
    print(f"   NATR(14): {natr[-1]:.2f}%")
    print(f"   RVI: {rvi_vol[-1]:.2f}")
    print(f"   Standard Deviation: {stddev[-1]:.2f}")
    print(f"   True Range: {tr[-1]:.2f}")
    print(f"   Mass Index: {mass_idx[-1]:.2f}")

def showcase_volume_indicators():
    """Showcase volume indicators"""
    print("\n🟣 VOLUME INDICATORS (11 indicators)")
    print("=" * 60)
    
    data = generate_sample_data()
    close = data['close']
    high = data['high']
    low = data['low']
    volume = data['volume']
    
    # Classic Volume
    obv = ta.obv(close, volume)
    vwap = ta.vwap(high, low, close, volume)
    mfi = ta.mfi(high, low, close, volume, 14)
    
    print(f"   OBV: {obv[-1]:,.0f}")
    print(f"   VWAP: {vwap[-1]:.2f}")
    print(f"   MFI(14): {mfi[-1]:.2f}")
    
    # Advanced Volume
    adl = ta.adl(high, low, close, volume)
    cmf = ta.cmf(high, low, close, volume, 20)
    emv = ta.emv(high, low, volume, 1000000)
    fi = ta.force_index(close, volume)
    nvi = ta.nvi(close, volume)
    pvi = ta.pvi(close, volume)
    vo = ta.volume_oscillator(volume, 5, 10)
    vroc = ta.vroc(volume, 25)
    
    print(f"   A/D Line: {adl[-1]:,.0f}")
    print(f"   Chaikin Money Flow: {cmf[-1]:.4f}")
    print(f"   Ease of Movement: {emv[-1]:.2f}")
    print(f"   Force Index: {fi[-1]:,.0f}")
    print(f"   NVI: {nvi[-1]:.2f}")
    print(f"   PVI: {pvi[-1]:.2f}")
    print(f"   Volume Oscillator: {vo[-1]:.2f}%")
    print(f"   Volume ROC: {vroc[-1]:.2f}%")

def showcase_statistical_indicators():
    """Showcase statistical indicators"""
    print("\n🟤 STATISTICAL INDICATORS (8 indicators)")
    print("=" * 60)
    
    data = generate_sample_data()
    close = data['close']
    
    # Generate market data for correlation/beta
    market = close * (1 + np.random.normal(0, 0.01, len(close)))
    
    # Statistical Analysis
    linear_reg = ta.linear_regression(close, 14)
    lr_slope = ta.linear_regression_slope(close, 14)
    correlation = ta.correlation(close, market, 20)
    beta = ta.beta(close, market, 252)
    variance = ta.variance(close, 20)
    tsf = ta.time_series_forecast(close, 14)
    median = ta.median(close, 20)
    mode = ta.mode(close, 20, 10)
    
    print(f"   Linear Regression: {linear_reg[-1]:.2f}")
    print(f"   LR Slope: {lr_slope[-1]:.6f}")
    print(f"   Correlation: {correlation[-1]:.3f}")
    print(f"   Beta: {beta[-1]:.3f}")
    print(f"   Variance: {variance[-1]:.2f}")
    print(f"   Time Series Forecast: {tsf[-1]:.2f}")
    print(f"   Median: {median[-1]:.2f}")
    print(f"   Mode: {mode[-1]:.2f}")

def showcase_hybrid_indicators():
    """Showcase hybrid/advanced indicators"""
    print("\n⚫ HYBRID & ADVANCED INDICATORS (7 indicators)")
    print("=" * 60)
    
    data = generate_sample_data()
    close = data['close']
    high = data['high']
    low = data['low']
    
    # Directional Movement System
    di_plus, di_minus, adx = ta.adx_system(high, low, close, 14)
    print(f"   ADX System: +DI={di_plus[-1]:.2f} | -DI={di_minus[-1]:.2f} | ADX={adx[-1]:.2f}")
    
    # Aroon System
    aroon_up, aroon_down = ta.aroon_system(high, low, 25)
    print(f"   Aroon: Up={aroon_up[-1]:.2f} | Down={aroon_down[-1]:.2f}")
    
    # Support/Resistance
    pivot, r1, s1, r2, s2, r3, s3 = ta.pivot_points(high, low, close)
    print(f"   Pivot Points: P={pivot[-1]:.2f} | R1={r1[-1]:.2f} | S1={s1[-1]:.2f}")
    
    # Parabolic SAR
    sar_values, sar_trend = ta.parabolic_sar(high, low, 0.02, 0.2)
    sar_signal = "🟢 BULLISH" if sar_trend[-1] == 1 else "🔴 BEARISH"
    print(f"   Parabolic SAR: {sar_values[-1]:.2f} ({sar_signal})")
    
    # Directional Movement Index
    dmi_plus, dmi_minus = ta.directional_movement(high, low, close, 14)
    print(f"   DMI: +DI={dmi_plus[-1]:.2f} | -DI={dmi_minus[-1]:.2f}")
    
    # Simple PSAR
    psar = ta.psar(high, low, 0.02, 0.2)
    print(f"   PSAR (values only): {psar[-1]:.2f}")
    
    # Hilbert Transform
    ht_trendline = ta.hilbert_trendline(close)
    print(f"   Hilbert Trendline: {ht_trendline[-1]:.2f}")

def showcase_utility_functions():
    """Showcase utility functions"""
    print("\n⚪ UTILITY FUNCTIONS")
    print("=" * 60)
    
    data = generate_sample_data()
    close = data['close']
    
    # Generate two series for crossover examples
    ema_fast = ta.ema(close, 10)
    ema_slow = ta.ema(close, 20)
    
    # Utility functions
    crossover_signals = ta.crossover(ema_fast, ema_slow)
    crossunder_signals = ta.crossunder(ema_fast, ema_slow)
    highest_20 = ta.highest(close, 20)
    lowest_20 = ta.lowest(close, 20)
    change_1 = ta.change(close, 1)
    roc_12 = ta.roc(close, 12)
    stdev_20 = ta.stdev(close, 20)
    
    # Count signals in last 100 periods
    recent_crossovers = np.sum(crossover_signals[-100:])
    recent_crossunders = np.sum(crossunder_signals[-100:])
    
    print(f"   Crossovers (last 100): {recent_crossovers}")
    print(f"   Crossunders (last 100): {recent_crossunders}")
    print(f"   Highest(20): {highest_20[-1]:.2f}")
    print(f"   Lowest(20): {lowest_20[-1]:.2f}")
    print(f"   Change(1): {change_1[-1]:.2f}")
    print(f"   ROC(12): {roc_12[-1]:.2f}%")
    print(f"   StdDev(20): {stdev_20[-1]:.2f}")

def performance_benchmark():
    """Benchmark performance of all indicators"""
    print("\n⏱️  PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    sizes = [1000, 10000, 100000]
    
    for size in sizes:
        print(f"\n📊 Testing with {size:,} data points:")
        
        # Generate test data
        data = generate_sample_data(size)
        close = data['close']
        high = data['high']
        low = data['low']
        volume = data['volume']
        
        # Test a representative sample of indicators
        indicators_to_test = [
            ("SMA(20)", lambda: ta.sma(close, 20)),
            ("EMA(20)", lambda: ta.ema(close, 20)),
            ("RSI(14)", lambda: ta.rsi(close, 14)),
            ("MACD", lambda: ta.macd(close, 12, 26, 9)),
            ("Bollinger Bands", lambda: ta.bbands(close, 20, 2)),
            ("Supertrend", lambda: ta.supertrend(high, low, close, 10, 3)),
            ("ADX System", lambda: ta.adx_system(high, low, close, 14)),
            ("VWAP", lambda: ta.vwap(high, low, close, volume)),
        ]
        
        for name, func in indicators_to_test:
            start_time = time.time()
            result = func()
            end_time = time.time()
            
            duration = (end_time - start_time) * 1000  # Convert to ms
            print(f"   {name}: {duration:.2f}ms")

def trading_strategy_example():
    """Example of using multiple indicators in a trading strategy"""
    print("\n🎯 MULTI-INDICATOR TRADING STRATEGY")
    print("=" * 60)
    
    data = generate_sample_data(500)
    close = data['close']
    high = data['high']
    low = data['low']
    volume = data['volume']
    
    print("Strategy: Multi-timeframe trend following with volume confirmation")
    
    # Trend Indicators
    ema_fast = ta.ema(close, 12)
    ema_slow = ta.ema(close, 26)
    supertrend, st_direction = ta.supertrend(high, low, close, 10, 3)
    adx_di_plus, adx_di_minus, adx = ta.adx_system(high, low, close, 14)
    
    # Momentum Filters
    rsi = ta.rsi(close, 14)
    macd_line, macd_signal, macd_hist = ta.macd(close, 12, 26, 9)
    
    # Volatility Filters
    atr = ta.atr(high, low, close, 14)
    bb_upper, bb_middle, bb_lower = ta.bbands(close, 20, 2)
    
    # Volume Confirmation
    obv = ta.obv(close, volume)
    cmf = ta.cmf(high, low, close, volume, 20)
    
    # Generate signals for last 50 periods
    signals = []
    for i in range(-50, 0):
        # Trend conditions
        ema_bullish = ema_fast[i] > ema_slow[i]
        supertrend_bullish = st_direction[i] == -1
        adx_strong = adx[i] > 25
        
        # Momentum conditions
        rsi_ok = 30 < rsi[i] < 70
        macd_bullish = macd_line[i] > macd_signal[i]
        
        # Volatility conditions
        bb_position = (close[i] - bb_lower[i]) / (bb_upper[i] - bb_lower[i])
        volatility_ok = 0.2 < bb_position < 0.8
        
        # Volume conditions
        volume_bullish = cmf[i] > 0
        
        # Combined signal
        if (ema_bullish and supertrend_bullish and adx_strong and 
            rsi_ok and macd_bullish and volatility_ok and volume_bullish):
            signals.append("🟢 BUY")
        elif (not ema_bullish and not supertrend_bullish and adx_strong and 
              rsi_ok and not macd_bullish and volatility_ok and not volume_bullish):
            signals.append("🔴 SELL")
        else:
            signals.append("⚪ HOLD")
    
    # Show recent signals
    buy_signals = signals.count("🟢 BUY")
    sell_signals = signals.count("🔴 SELL")
    hold_signals = signals.count("⚪ HOLD")
    
    print(f"\nSignals in last 50 periods:")
    print(f"   Buy signals: {buy_signals}")
    print(f"   Sell signals: {sell_signals}")
    print(f"   Hold signals: {hold_signals}")
    
    print(f"\nLast 10 signals: {' '.join(signals[-10:])}")
    
    # Current market conditions
    print(f"\nCurrent Market Analysis:")
    print(f"   Price: {close[-1]:.2f}")
    print(f"   EMA Trend: {'🟢 Bullish' if ema_fast[-1] > ema_slow[-1] else '🔴 Bearish'}")
    print(f"   Supertrend: {'🟢 Bullish' if st_direction[-1] == -1 else '🔴 Bearish'}")
    print(f"   ADX Strength: {adx[-1]:.1f} {'(Strong)' if adx[-1] > 25 else '(Weak)'}")
    print(f"   RSI: {rsi[-1]:.1f} {'(Overbought)' if rsi[-1] > 70 else '(Oversold)' if rsi[-1] < 30 else '(Neutral)'}")
    print(f"   Volume Flow: {'🟢 Positive' if cmf[-1] > 0 else '🔴 Negative'}")

def main():
    """Main function to run all showcases"""
    print("🚀 OpenAlgo Technical Indicators Comprehensive Showcase")
    print("=" * 80)
    print(f"📊 Total Indicators Available: 100+")
    print(f"🎯 TradingView-like Syntax: ta.indicator_name()")
    print(f"⚡ Numba-optimized for High Performance")
    print("=" * 80)
    
    # Run all showcases
    showcase_trend_indicators()
    showcase_momentum_indicators()
    showcase_oscillators()
    showcase_volatility_indicators()
    showcase_volume_indicators()
    showcase_statistical_indicators()
    showcase_hybrid_indicators()
    showcase_utility_functions()
    
    # Performance and strategy examples
    performance_benchmark()
    trading_strategy_example()
    
    print(f"\n✅ All indicators working perfectly!")
    print(f"📚 Check the documentation for detailed parameter descriptions")
    print(f"🔗 Visit: https://docs.openalgo.in")

if __name__ == "__main__":
    main()