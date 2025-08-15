#!/usr/bin/env python3
"""
Final verification of LRSLOPE against TradingView script
"""

import numpy as np
import pandas as pd
import sys
import os

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def test_lrslope_tradingview_defaults():
    """Test LRSLOPE with TradingView default settings"""
    
    print("LRSLOPE TradingView Verification")
    print("=" * 60)
    print("TradingView Script:")
    print("len = input(defval=100, minval=1, title='Linear Regression length')")
    print("linear_reg = linreg(close_price, len, 0)")  
    print("linear_reg_prev = linreg(close[1], len, 0)")
    print("slope = ((linear_reg - linear_reg_prev) / interval)")
    print()
    
    # Create test data with clear trend
    np.random.seed(42)
    n_periods = 150
    
    # Generate trending data
    base_price = 100
    prices = []
    for i in range(n_periods):
        if i == 0:
            price = base_price
        else:
            # Add slight upward trend with noise
            trend = 0.001  # 0.1% per period
            noise = np.random.normal(0, 0.02)  # 2% noise
            price = prices[-1] * (1 + trend + noise)
        prices.append(price)
    
    close_data = np.array(prices)
    
    print(f"Test data: {n_periods} periods")
    print(f"Price range: {close_data.min():.2f} - {close_data.max():.2f}")
    print(f"Price trend: {close_data[0]:.2f} -> {close_data[-1]:.2f}")
    print()
    
    # Test with TradingView defaults
    print("Testing with TradingView defaults:")
    print("  period = 100 (TradingView default)")
    print("  interval = 1 (daily timeframe)")
    
    try:
        # Test current implementation
        lrslope_result = ta.lrslope(close_data, period=100, interval=1)
        
        print(f"  LRSLOPE calculated successfully")
        print(f"  Result length: {len(lrslope_result)}")
        
        # Analyze results
        valid_values = lrslope_result[~np.isnan(lrslope_result)]
        print(f"  Valid values: {len(valid_values)}")
        
        if len(valid_values) > 0:
            print(f"  Value range: {valid_values.min():.6f} to {valid_values.max():.6f}")
            print(f"  Last 10 values: {lrslope_result[-10:]}")
            
            # Analyze trend detection
            positive_slopes = np.sum(valid_values > 0)
            negative_slopes = np.sum(valid_values <= 0)
            print(f"  Positive slopes: {positive_slopes} ({positive_slopes/len(valid_values)*100:.1f}%)")
            print(f"  Negative slopes: {negative_slopes} ({negative_slopes/len(valid_values)*100:.1f}%)")
            
            # Check if it detects the overall uptrend
            avg_slope = np.mean(valid_values)
            print(f"  Average slope: {avg_slope:.6f}")
            if avg_slope > 0:
                print("  OK: Detects upward trend correctly")
            else:
                print("  Note: Average slope is negative despite uptrend")
        
        print()
        
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_lrslope_signal_generation():
    """Test LRSLOPE signal generation like TradingView script"""
    
    print("Testing LRSLOPE Signal Generation (TradingView Logic)")
    print("=" * 60)
    print("TradingView Rules:")
    print("  bullishRule = slope > 0")
    print("  bearishRule = slope <= 0")
    print()
    
    # Create data with trend changes
    n_periods = 80
    
    # Generate data with distinct trend phases
    prices = [100]
    
    for i in range(1, n_periods):
        if i < 20:
            # Uptrend phase
            trend = 0.005
        elif i < 40:
            # Downtrend phase  
            trend = -0.003
        elif i < 60:
            # Sideways phase
            trend = 0.0
        else:
            # Strong uptrend phase
            trend = 0.008
        
        noise = np.random.normal(0, 0.01)
        new_price = prices[-1] * (1 + trend + noise)
        prices.append(new_price)
    
    close_data = np.array(prices)
    
    print(f"Data phases:")
    print(f"  0-19: Uptrend (trend=0.5%)")
    print(f"  20-39: Downtrend (trend=-0.3%)")
    print(f"  40-59: Sideways (trend=0%)")
    print(f"  60-79: Strong uptrend (trend=0.8%)")
    print()
    
    # Calculate LRSLOPE with shorter period for responsiveness
    lrslope_result = ta.lrslope(close_data, period=20, interval=1)
    
    # Apply TradingView signal rules
    bullish_signals = lrslope_result > 0
    bearish_signals = lrslope_result <= 0
    
    # Analyze signals by phase
    phases = [
        ("Uptrend", 0, 20),
        ("Downtrend", 20, 40), 
        ("Sideways", 40, 60),
        ("Strong Uptrend", 60, 80)
    ]
    
    print("Signal Analysis by Phase:")
    for phase_name, start, end in phases:
        phase_slopes = lrslope_result[start:end]
        phase_bullish = bullish_signals[start:end]
        phase_bearish = bearish_signals[start:end]
        
        valid_mask = ~np.isnan(phase_slopes)
        if np.sum(valid_mask) > 0:
            valid_slopes = phase_slopes[valid_mask]
            valid_bullish = phase_bullish[valid_mask]
            valid_bearish = phase_bearish[valid_mask]
            
            bullish_pct = np.sum(valid_bullish) / len(valid_bullish) * 100
            bearish_pct = np.sum(valid_bearish) / len(valid_bearish) * 100
            avg_slope = np.mean(valid_slopes)
            
            print(f"  {phase_name}: {bullish_pct:.1f}% bullish, {bearish_pct:.1f}% bearish, avg slope: {avg_slope:.6f}")

def test_lrslope_with_pandas():
    """Test LRSLOPE with pandas data"""
    
    print("\\nTesting LRSLOPE with Pandas")
    print("=" * 60)
    
    # Create pandas Series
    n = 120
    np.random.seed(456)
    
    data = []
    base_price = 100
    
    for i in range(n):
        trend = 0.002 * np.sin(i / 10)  # Cyclical trend
        noise = np.random.normal(0, 0.015)
        if i == 0:
            price = base_price
        else:
            price = data[-1] * (1 + trend + noise)
        data.append(price)
    
    close_series = pd.Series(data)
    
    try:
        lrslope_pandas = ta.lrslope(close_series, period=50, interval=1)
        
        print(f"  Pandas calculation successful!")
        print(f"  Result type: {type(lrslope_pandas)}")
        print(f"  Valid values: {np.sum(~pd.isna(lrslope_pandas))}/{len(lrslope_pandas)}")
        
        if np.sum(~pd.isna(lrslope_pandas)) > 0:
            valid_values = lrslope_pandas.dropna()
            print(f"  Value range: {valid_values.min():.6f} to {valid_values.max():.6f}")
            print(f"  Last 5 values: {lrslope_pandas.tail().values}")
        
    except Exception as e:
        print(f"  ERROR with pandas: {e}")

def test_lrslope_parameter_validation():
    """Test parameter validation"""
    
    print("\\nTesting Parameter Validation")
    print("=" * 60)
    
    close_data = np.array([100, 101, 99, 102, 98, 103] * 20)  # 120 periods
    
    # Test valid parameters
    try:
        result = ta.lrslope(close_data, period=100, interval=1)
        print(f"  OK: Valid parameters accepted")
    except Exception as e:
        print(f"  ERROR: Valid parameters rejected: {e}")
    
    # Test invalid period
    try:
        result = ta.lrslope(close_data, period=0)
        print("  ERROR: Should have failed with period=0")
    except ValueError as e:
        print(f"  OK: Period validation working: {e}")
    
    # Test invalid interval
    try:
        result = ta.lrslope(close_data, period=10, interval=0)
        print("  ERROR: Should have failed with interval=0")
    except ValueError as e:
        print(f"  OK: Interval validation working: {e}")
    
    # Test insufficient data
    try:
        short_data = np.array([100, 101, 102])
        result = ta.lrslope(short_data, period=10)
        print("  ERROR: Should have failed with insufficient data")
    except ValueError as e:
        print(f"  OK: Data length validation working: {e}")

if __name__ == "__main__":
    test_lrslope_tradingview_defaults()
    test_lrslope_signal_generation()
    test_lrslope_with_pandas()
    test_lrslope_parameter_validation()