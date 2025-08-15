#!/usr/bin/env python3
"""
Test KAMA implementation against TradingView logic
"""

import numpy as np
import pandas as pd
import sys
import os

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def test_kama_basic():
    """Test the KAMA implementation with sample data"""
    
    print("Testing KAMA Implementation...")
    print("=" * 60)
    
    # Create sample price data with varying volatility
    np.random.seed(42)
    n_periods = 100
    
    # Generate realistic price data with different volatility regimes
    base_price = 100
    prices = [base_price]
    
    for i in range(1, n_periods):
        # Create volatility regimes
        if i < 30:
            vol = 0.5  # Low volatility - trending
        elif i < 60:
            vol = 2.0  # High volatility - choppy  
        else:
            vol = 1.0  # Medium volatility
        
        # Add some trend
        trend = 0.02 if i < 50 else -0.01
        
        # Random walk with changing volatility
        change = np.random.normal(trend, vol / 100)
        new_price = prices[-1] * (1 + change)
        prices.append(max(1, new_price))
    
    close_prices = np.array(prices)
    
    print(f"Generated {n_periods} periods of test data")
    print(f"Price range: {close_prices.min():.2f} - {close_prices.max():.2f}")
    print(f"Price trend: {close_prices[0]:.2f} -> {close_prices[-1]:.2f}")
    print()
    
    # Test with TradingView default parameters
    try:
        print("Testing with TradingView defaults (length=14, fastLength=2, slowLength=30)...")
        
        kama_result = ta.kama(close_prices)
        
        print(f"  KAMA calculated successfully")
        print(f"  Result length: {len(kama_result)}")
        print(f"  Non-NaN values: {np.sum(~np.isnan(kama_result))}")
        
        # Find first valid value
        first_valid = np.argmax(~np.isnan(kama_result))
        print(f"  First valid value at index: {first_valid}")
        
        if np.sum(~np.isnan(kama_result)) > 0:
            valid_kama = kama_result[~np.isnan(kama_result)]
            print(f"  KAMA range: {valid_kama.min():.2f} - {valid_kama.max():.2f}")
            print(f"  Last 5 values: {kama_result[-5:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR: {e}")
        print()
    
    # Test with custom parameters
    try:
        print("Testing with custom parameters (length=10, fastLength=3, slowLength=20)...")
        
        kama_custom = ta.kama(close_prices, length=10, fast_length=3, slow_length=20)
        
        print(f"  Custom KAMA calculated successfully")
        print(f"  Non-NaN values: {np.sum(~np.isnan(kama_custom))}")
        
        if np.sum(~np.isnan(kama_custom)) > 0:
            valid_kama_custom = kama_custom[~np.isnan(kama_custom)]
            print(f"  Custom KAMA range: {valid_kama_custom.min():.2f} - {valid_kama_custom.max():.2f}")
            print(f"  Last 5 values: {kama_custom[-5:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR with custom parameters: {e}")
        print()

def test_kama_tradingview_comparison():
    """Test specific values that can be manually verified against TradingView"""
    print("Testing TradingView Formula Accuracy...")
    print("=" * 60)
    
    # Use simple test data for manual verification
    close_prices = np.array([100.0, 102.0, 98.0, 105.0, 95.0, 110.0, 90.0, 108.0, 92.0, 106.0, 
                            94.0, 112.0, 88.0, 115.0, 85.0, 118.0, 82.0, 120.0])
    
    print(f"Test data: {close_prices}")
    print()
    
    # Calculate with small length for easier verification
    kama_result = ta.kama(close_prices, length=5, fast_length=2, slow_length=10)
    
    print(f"KAMA result: {kama_result}")
    print()
    
    # Manual calculation for verification (TradingView logic)
    length = 5
    fast_length = 2
    slow_length = 10
    
    print("Manual TradingView calculation verification:")
    print("TradingView formula:")
    print("mom = abs(change(src, length))")
    print("volatility = sum(abs(change(src)), length)")
    print("er = volatility != 0 ? mom / volatility : 0")
    print("fastAlpha = 2 / (fastLength + 1)")
    print("slowAlpha = 2 / (slowLength + 1)")
    print("alpha = pow(er * (fastAlpha - slowAlpha) + slowAlpha, 2)")
    print("kama = alpha * src + (1 - alpha) * nz(kama[1], src)")
    print()
    
    if len(close_prices) >= length + 1:
        i = length  # First calculation point
        
        # Manual calculation for first KAMA value
        mom = abs(close_prices[i] - close_prices[i - length])
        print(f"At index {i}:")
        print(f"  mom = abs({close_prices[i]:.1f} - {close_prices[i-length]:.1f}) = {mom:.2f}")
        
        volatility = 0.0
        for j in range(i - length + 1, i + 1):
            if j > 0:
                change = abs(close_prices[j] - close_prices[j - 1])
                volatility += change
                print(f"  volatility += abs({close_prices[j]:.1f} - {close_prices[j-1]:.1f}) = {change:.2f}")
        
        print(f"  Total volatility = {volatility:.2f}")
        
        if volatility != 0:
            er = mom / volatility
        else:
            er = 0.0
        print(f"  er = {mom:.2f} / {volatility:.2f} = {er:.4f}")
        
        fast_alpha = 2.0 / (fast_length + 1)
        slow_alpha = 2.0 / (slow_length + 1)
        print(f"  fastAlpha = 2 / ({fast_length} + 1) = {fast_alpha:.4f}")
        print(f"  slowAlpha = 2 / ({slow_length} + 1) = {slow_alpha:.4f}")
        
        alpha = (er * (fast_alpha - slow_alpha) + slow_alpha) ** 2
        print(f"  alpha = ({er:.4f} * ({fast_alpha:.4f} - {slow_alpha:.4f}) + {slow_alpha:.4f})^2 = {alpha:.6f}")
        
        # First KAMA uses current price as previous (nz logic)
        kama_manual = alpha * close_prices[i] + (1 - alpha) * close_prices[i]
        print(f"  kama = {alpha:.6f} * {close_prices[i]:.1f} + (1 - {alpha:.6f}) * {close_prices[i]:.1f} = {kama_manual:.6f}")
        print(f"  Function result: {kama_result[i]:.6f}")
        print(f"  Difference: {abs(kama_manual - kama_result[i]):.8f}")

def test_kama_adaptiveness():
    """Test KAMA's adaptive behavior in different market conditions"""
    print("\\nTesting KAMA Adaptive Behavior...")
    print("=" * 60)
    
    # Create data with distinct trending vs choppy periods
    n_periods = 100
    
    # Trending period (low volatility, high efficiency)
    trending_data = np.linspace(100, 120, 50)  # Smooth uptrend
    
    # Choppy period (high volatility, low efficiency)
    np.random.seed(42)
    choppy_data = 120 + np.random.normal(0, 2, 50)  # High volatility around 120
    
    combined_data = np.concatenate([trending_data, choppy_data])
    
    print(f"Data: 50 periods trending (100->120), 50 periods choppy (120±2)")
    
    # Calculate KAMA
    kama_result = ta.kama(combined_data, length=10, fast_length=2, slow_length=20)
    
    # Analyze behavior in different periods
    trending_kama = kama_result[10:50]  # Skip initial NaN values
    choppy_kama = kama_result[50:100]
    
    trending_valid = trending_kama[~np.isnan(trending_kama)]
    choppy_valid = choppy_kama[~np.isnan(choppy_kama)]
    
    if len(trending_valid) > 1 and len(choppy_valid) > 1:
        # Calculate responsiveness (how much KAMA changes)
        trending_changes = np.abs(np.diff(trending_valid))
        choppy_changes = np.abs(np.diff(choppy_valid))
        
        print(f"\\nAdaptive behavior analysis:")
        print(f"  Trending period:")
        print(f"    Average KAMA change: {np.mean(trending_changes):.4f}")
        print(f"    Max KAMA change: {np.max(trending_changes):.4f}")
        print(f"  Choppy period:")
        print(f"    Average KAMA change: {np.mean(choppy_changes):.4f}")
        print(f"    Max KAMA change: {np.max(choppy_changes):.4f}")
        
        # KAMA should be more responsive (larger changes) in trending markets
        # and less responsive (smaller changes) in choppy markets
        if np.mean(trending_changes) > np.mean(choppy_changes):
            print(f"  OK: KAMA correctly adapts: more responsive in trending market")
        else:
            print(f"  WARNING: KAMA adaptation may need verification")

def test_with_pandas():
    """Test with pandas data"""
    print("\\nTesting with Pandas Series...")
    print("=" * 60)
    
    # Create test data
    n = 50
    np.random.seed(456)
    
    # Generate price series with trend
    prices = []
    base_price = 100
    for i in range(n):
        trend = 0.01  # 1% trend
        noise = np.random.normal(0, 0.02)  # 2% noise
        if i == 0:
            price = base_price
        else:
            price = prices[-1] * (1 + trend + noise)
        prices.append(max(1, price))
    
    # Convert to pandas
    close_series = pd.Series(prices)
    
    try:
        kama_pandas = ta.kama(close_series, length=14, fast_length=2, slow_length=30)
        
        print(f"  Pandas calculation successful!")
        print(f"  Result type: {type(kama_pandas)}")
        print(f"  Valid KAMA values: {np.sum(~pd.isna(kama_pandas))}/{len(kama_pandas)}")
        
        if np.sum(~pd.isna(kama_pandas)) > 0:
            valid_values = kama_pandas.dropna()
            print(f"  KAMA range: {valid_values.min():.2f} - {valid_values.max():.2f}")
            print(f"  Last 5 values: {kama_pandas.tail().values}")
        
    except Exception as e:
        print(f"  ERROR with pandas: {e}")

def test_parameter_validation():
    """Test parameter validation"""
    print("\\nTesting Parameter Validation...")
    print("=" * 60)
    
    # Create minimal test data
    close_prices = np.array([100, 101, 99, 102, 98, 103, 97, 104, 96, 105, 95, 106, 94, 107, 93, 108])
    
    # Test invalid length
    try:
        kama_invalid = ta.kama(close_prices, length=0)
        print("  ERROR: Should have failed with length=0")
    except ValueError as e:
        print(f"  OK: Length validation working: {e}")
    
    # Test invalid fast_length
    try:
        kama_invalid = ta.kama(close_prices, length=10, fast_length=0)
        print("  ERROR: Should have failed with fast_length=0")
    except ValueError as e:
        print(f"  OK: Fast length validation working: {e}")
    
    # Test fast_length >= slow_length
    try:
        kama_invalid = ta.kama(close_prices, length=10, fast_length=20, slow_length=10)
        print("  ERROR: Should have failed with fast_length >= slow_length")
    except ValueError as e:
        print(f"  OK: Fast/slow length validation working: {e}")
    
    # Test insufficient data
    try:
        short_data = np.array([100, 101, 102])
        kama_short = ta.kama(short_data, length=10)
        print("  ERROR: Should have failed with insufficient data")
    except ValueError as e:
        print(f"  OK: Data length validation working: {e}")

if __name__ == "__main__":
    test_kama_basic()
    test_kama_tradingview_comparison()
    test_kama_adaptiveness()
    test_with_pandas()
    test_parameter_validation()