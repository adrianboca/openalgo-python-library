#!/usr/bin/env python3
"""
Test KVO implementation against TradingView logic
"""

import numpy as np
import pandas as pd
import sys
import os

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def test_kvo_basic():
    """Test the KVO implementation with sample data"""
    
    print("Testing KVO Implementation...")
    print("=" * 60)
    
    # Create sample OHLC data with volume
    np.random.seed(42)
    n_periods = 100
    
    # Generate realistic OHLC data with volume patterns
    base_price = 100
    base_volume = 1000000
    
    high_prices = []
    low_prices = []
    close_prices = []
    volumes = []
    
    for i in range(n_periods):
        # Create price trends with corresponding volume patterns
        if i < 30:
            # Uptrend with increasing volume
            price_trend = 0.01
            volume_mult = 1.0 + (i / 30) * 0.5  # Volume increases with trend
        elif i < 60:
            # Sideways with decreasing volume
            price_trend = 0.0
            volume_mult = 1.5 - (i - 30) / 30 * 0.3  # Volume decreases
        else:
            # Downtrend with high volume
            price_trend = -0.015
            volume_mult = 1.2 + np.random.uniform(0, 0.8)  # High, volatile volume
        
        # Generate price
        if i == 0:
            close = base_price
        else:
            change = np.random.normal(price_trend, 0.015)
            close = close_prices[-1] * (1 + change)
        
        # Generate realistic OHLC
        daily_range = abs(np.random.normal(0, 0.02)) * close
        high = close + daily_range * np.random.uniform(0.3, 0.7)
        low = close - daily_range * np.random.uniform(0.3, 0.7)
        
        # Ensure OHLC consistency
        high = max(high, close)
        low = min(low, close)
        
        # Generate volume
        volume = int(base_volume * volume_mult * (1 + np.random.normal(0, 0.3)))
        volume = max(100000, volume)  # Minimum volume
        
        high_prices.append(high)
        low_prices.append(low)
        close_prices.append(close)
        volumes.append(volume)
    
    high_data = np.array(high_prices)
    low_data = np.array(low_prices)
    close_data = np.array(close_prices)
    volume_data = np.array(volumes)
    
    print(f"Generated {n_periods} periods of OHLCV data")
    print(f"Price range: {close_data.min():.2f} - {close_data.max():.2f}")
    print(f"Volume range: {volume_data.min():.0f} - {volume_data.max():.0f}")
    print(f"Price trend: {close_data[0]:.2f} -> {close_data[-1]:.2f}")
    print()
    
    # Test with TradingView default parameters
    try:
        print("Testing with TradingView defaults...")
        print("TrigLen=13, FastX=34, SlowX=55")
        
        kvo_result, trigger_result = ta.kvo(high_data, low_data, close_data, volume_data)
        
        print(f"  KVO calculated successfully")
        print(f"  Result length: {len(kvo_result)}")
        print(f"  KVO Non-NaN values: {np.sum(~np.isnan(kvo_result))}")
        print(f"  Trigger Non-NaN values: {np.sum(~np.isnan(trigger_result))}")
        
        # Find first valid values
        first_valid_kvo = np.argmax(~np.isnan(kvo_result))
        first_valid_trigger = np.argmax(~np.isnan(trigger_result))
        print(f"  First valid KVO at index: {first_valid_kvo}")
        print(f"  First valid Trigger at index: {first_valid_trigger}")
        
        if np.sum(~np.isnan(kvo_result)) > 0:
            valid_kvo = kvo_result[~np.isnan(kvo_result)]
            print(f"  KVO range: {valid_kvo.min():.0f} - {valid_kvo.max():.0f}")
            print(f"  Last 5 KVO values: {kvo_result[-5:]}")
        
        if np.sum(~np.isnan(trigger_result)) > 0:
            valid_trigger = trigger_result[~np.isnan(trigger_result)]
            print(f"  Trigger range: {valid_trigger.min():.0f} - {valid_trigger.max():.0f}")
            print(f"  Last 5 Trigger values: {trigger_result[-5:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR: {e}")
        print()

def test_kvo_tradingview_comparison():
    """Test specific values that can be manually verified against TradingView"""
    print("Testing TradingView Formula Accuracy...")
    print("=" * 60)
    
    # Use simple test data for manual verification
    high_data = np.array([105.0, 107.0, 103.0, 109.0, 101.0, 112.0, 98.0, 115.0, 95.0, 118.0])
    low_data = np.array([95.0, 97.0, 93.0, 99.0, 91.0, 102.0, 88.0, 105.0, 85.0, 108.0])
    close_data = np.array([100.0, 102.0, 98.0, 104.0, 96.0, 107.0, 93.0, 110.0, 90.0, 113.0])
    volume_data = np.array([1000.0, 1100.0, 900.0, 1200.0, 800.0, 1300.0, 700.0, 1400.0, 600.0, 1500.0])
    
    print(f"Test data: {len(close_data)} periods")
    print(f"Price: {close_data}")
    print(f"Volume: {volume_data}")
    print()
    
    # Calculate with small periods for easier verification
    try:
        kvo_result, trigger_result = ta.kvo(
            high_data, low_data, close_data, volume_data,
            13, 5, 8  # Use positional args to avoid keyword issues
        )
    except Exception as e:
        print(f"ERROR in kvo calculation: {e}")
        return
    
    print("TradingView Logic Verification:")
    print("xTrend = iff(hlc3 > hlc3[1], volume * 100, -volume * 100)")
    print("xFast = ema(xTrend, FastX)")
    print("xSlow = ema(xTrend, SlowX)")
    print("xKVO = xFast - xSlow")
    print("xTrigger = ema(xKVO, TrigLen)")
    print()
    
    # Manual verification of hlc3 logic
    hlc3 = (high_data + low_data + close_data) / 3.0
    print(f"hlc3 values: {hlc3}")
    
    # Manual calculation of xTrend for first few values
    print("\\nManual xTrend calculation:")
    for i in range(min(5, len(hlc3))):
        if i == 0:
            trend_val = volume_data[i] * 100  # Assume positive for first value
            print(f"  Index {i}: xTrend = {volume_data[i]:.0f} * 100 = {trend_val:.0f} (first value)")
        else:
            if hlc3[i] > hlc3[i-1]:
                trend_val = volume_data[i] * 100
                comparison = ">"
            else:
                trend_val = -volume_data[i] * 100
                comparison = "<="
            print(f"  Index {i}: hlc3[{i}] {comparison} hlc3[{i-1}] ({hlc3[i]:.2f} {comparison} {hlc3[i-1]:.2f}) -> xTrend = {trend_val:.0f}")
    
    print(f"\\nKVO result: {kvo_result}")
    print(f"Trigger result: {trigger_result}")

def test_kvo_volume_price_relationship():
    """Test KVO's ability to detect volume-price relationships"""
    print("\\nTesting KVO Volume-Price Relationship Detection...")
    print("=" * 60)
    
    # Create data with specific volume-price patterns
    n_periods = 60
    
    # Pattern 1: Price up, volume up (bullish)
    pattern1_close = np.linspace(100, 120, 20)  
    pattern1_volume = np.linspace(1000, 2000, 20)
    
    # Pattern 2: Price up, volume down (bearish divergence)
    pattern2_close = np.linspace(120, 130, 20)
    pattern2_volume = np.linspace(2000, 500, 20)
    
    # Pattern 3: Price down, volume up (potential reversal)
    pattern3_close = np.linspace(130, 110, 20)
    pattern3_volume = np.linspace(500, 1800, 20)
    
    combined_close = np.concatenate([pattern1_close, pattern2_close, pattern3_close])
    combined_volume = np.concatenate([pattern1_volume, pattern2_volume, pattern3_volume])
    
    # Generate corresponding high/low
    combined_high = combined_close * (1 + np.random.uniform(0.005, 0.015, len(combined_close)))
    combined_low = combined_close * (1 - np.random.uniform(0.005, 0.015, len(combined_close)))
    
    print(f"Data patterns:")
    print(f"  Pattern 1 (0-19): Price up (100->120), Volume up (1000->2000)")
    print(f"  Pattern 2 (20-39): Price up (120->130), Volume down (2000->500)")
    print(f"  Pattern 3 (40-59): Price down (130->110), Volume up (500->1800)")
    
    # Calculate KVO
    kvo_result, trigger_result = ta.kvo(combined_high, combined_low, combined_close, combined_volume)
    
    # Analyze KVO behavior in different patterns
    if np.sum(~np.isnan(kvo_result)) > 0:
        valid_indices = ~np.isnan(kvo_result)
        valid_kvo = kvo_result[valid_indices]
        valid_positions = np.where(valid_indices)[0]
        
        pattern1_kvo = []
        pattern2_kvo = []
        pattern3_kvo = []
        
        for i, pos in enumerate(valid_positions):
            if pos < 20:  # Pattern 1
                pattern1_kvo.append(valid_kvo[i])
            elif pos < 40:  # Pattern 2
                pattern2_kvo.append(valid_kvo[i])
            else:  # Pattern 3
                pattern3_kvo.append(valid_kvo[i])
        
        print(f"\\nKVO analysis:")
        if pattern1_kvo:
            trend1 = "Up" if pattern1_kvo[-1] > pattern1_kvo[0] else "Down"
            print(f"  Pattern 1 (Price UP, Volume UP): KVO {trend1} ({pattern1_kvo[0]:.0f} -> {pattern1_kvo[-1]:.0f})")
        if pattern2_kvo:
            trend2 = "Up" if pattern2_kvo[-1] > pattern2_kvo[0] else "Down"
            print(f"  Pattern 2 (Price UP, Volume DOWN): KVO {trend2} ({pattern2_kvo[0]:.0f} -> {pattern2_kvo[-1]:.0f})")
        if pattern3_kvo:
            trend3 = "Up" if pattern3_kvo[-1] > pattern3_kvo[0] else "Down"
            print(f"  Pattern 3 (Price DOWN, Volume UP): KVO {trend3} ({pattern3_kvo[0]:.0f} -> {pattern3_kvo[-1]:.0f})")

def test_with_pandas():
    """Test with pandas data"""
    print("\\nTesting with Pandas Series...")
    print("=" * 60)
    
    # Create test data
    n = 50
    np.random.seed(456)
    
    # Generate OHLCV data
    data = []
    base_price = 100
    base_volume = 1000000
    
    for i in range(n):
        trend = 0.002 * np.sin(i / 10)  # Cyclical trend
        noise = np.random.normal(0, 0.015)
        volume_trend = 1 + 0.3 * np.sin(i / 8)  # Volume cycles
        
        if i == 0:
            close = base_price
        else:
            close = data[-1]['close'] * (1 + trend + noise)
        
        # Generate OHLC
        daily_range = abs(np.random.normal(0, 0.02)) * close
        high = close + daily_range * 0.6
        low = close - daily_range * 0.4
        volume = int(base_volume * volume_trend * (1 + np.random.normal(0, 0.2)))
        
        data.append({
            'high': high,
            'low': low, 
            'close': close,
            'volume': max(100000, volume)
        })
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    
    try:
        kvo_pandas, trigger_pandas = ta.kvo(df['high'], df['low'], df['close'], df['volume'])
        
        print(f"  Pandas calculation successful!")
        print(f"  Result types: {type(kvo_pandas).__name__}, {type(trigger_pandas).__name__}")
        print(f"  Valid KVO values: {np.sum(~pd.isna(kvo_pandas))}/{len(kvo_pandas)}")
        print(f"  Valid Trigger values: {np.sum(~pd.isna(trigger_pandas))}/{len(trigger_pandas)}")
        
        if np.sum(~pd.isna(kvo_pandas)) > 0:
            valid_kvo = kvo_pandas.dropna()
            valid_trigger = trigger_pandas.dropna()
            print(f"  KVO range: {valid_kvo.min():.0f} - {valid_kvo.max():.0f}")
            print(f"  Trigger range: {valid_trigger.min():.0f} - {valid_trigger.max():.0f}")
            print(f"  Last 3 KVO values: {kvo_pandas.tail(3).values}")
            print(f"  Last 3 Trigger values: {trigger_pandas.tail(3).values}")
        
    except Exception as e:
        print(f"  ERROR with pandas: {e}")

def test_parameter_validation():
    """Test parameter validation"""
    print("\\nTesting Parameter Validation...")
    print("=" * 60)
    
    # Create minimal test data
    high_data = np.array([102, 103, 101, 104, 100, 105] * 10)  # 60 periods
    low_data = np.array([98, 99, 97, 100, 96, 101] * 10)
    close_data = np.array([100, 101, 99, 102, 98, 103] * 10) 
    volume_data = np.array([1000, 1100, 900, 1200, 800, 1300] * 10)
    
    # Test invalid trig_len
    try:
        kvo_invalid = ta.kvo(high_data, low_data, close_data, volume_data, trig_len=0)
        print("  ERROR: Should have failed with trig_len=0")
    except ValueError as e:
        print(f"  OK: Trigger length validation working: {e}")
    
    # Test invalid fast_x
    try:
        kvo_invalid = ta.kvo(high_data, low_data, close_data, volume_data, fast_x=0)
        print("  ERROR: Should have failed with fast_x=0")
    except ValueError as e:
        print(f"  OK: Fast X validation working: {e}")
    
    # Test invalid slow_x
    try:
        kvo_invalid = ta.kvo(high_data, low_data, close_data, volume_data, slow_x=-5)
        print("  ERROR: Should have failed with slow_x=-5")
    except ValueError as e:
        print(f"  OK: Slow X validation working: {e}")

def test_kvo_signal_crossovers():
    """Test KVO and Trigger line crossovers"""
    print("\\nTesting KVO Signal Crossovers...")
    print("=" * 60)
    
    # Create data with volume/price patterns that should generate clear signals
    n = 80
    
    # Create cyclical price and volume data
    prices = []
    volumes = []
    
    for i in range(n):
        # Price cycle
        price_cycle = 100 + 15 * np.sin(i / 15)
        price_noise = np.random.normal(0, 2)
        price = price_cycle + price_noise
        
        # Volume cycle (somewhat related to price changes)
        volume_base = 1000000
        volume_cycle = 0.8 + 0.4 * np.sin((i + 5) / 12)  # Phase shift from price
        volume = int(volume_base * volume_cycle * (1 + np.random.normal(0, 0.3)))
        volume = max(100000, volume)
        
        prices.append(price)
        volumes.append(volume)
    
    close_data = np.array(prices)
    high_data = close_data * (1 + np.random.uniform(0.001, 0.02, len(close_data)))
    low_data = close_data * (1 - np.random.uniform(0.001, 0.02, len(close_data)))
    volume_data = np.array(volumes)
    
    try:
        kvo_result, trigger_result = ta.kvo(high_data, low_data, close_data, volume_data)
        
        # Find crossovers
        valid_mask = ~(np.isnan(kvo_result) | np.isnan(trigger_result))
        if np.sum(valid_mask) > 1:
            valid_kvo = kvo_result[valid_mask]
            valid_trigger = trigger_result[valid_mask]
            
            # Find crossovers
            bullish_crossovers = []
            bearish_crossovers = []
            
            for i in range(1, len(valid_kvo)):
                if valid_kvo[i-1] <= valid_trigger[i-1] and valid_kvo[i] > valid_trigger[i]:
                    bullish_crossovers.append(i)
                elif valid_kvo[i-1] >= valid_trigger[i-1] and valid_kvo[i] < valid_trigger[i]:
                    bearish_crossovers.append(i)
            
            print(f"  Valid data points: {len(valid_kvo)}")
            print(f"  Bullish crossovers found: {len(bullish_crossovers)}")
            print(f"  Bearish crossovers found: {len(bearish_crossovers)}")
            print(f"  KVO range: {valid_kvo.min():.0f} - {valid_kvo.max():.0f}")
            print(f"  Trigger range: {valid_trigger.min():.0f} - {valid_trigger.max():.0f}")
            
            if bullish_crossovers or bearish_crossovers:
                print(f"  OK: KVO generates crossover signals")
            else:
                print(f"  Note: No crossovers detected in test data")
        
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    test_kvo_basic()
    test_kvo_tradingview_comparison()
    test_kvo_volume_price_relationship()
    test_with_pandas()
    test_parameter_validation()
    test_kvo_signal_crossovers()