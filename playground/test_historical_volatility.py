#!/usr/bin/env python3
"""
Test Historical Volatility implementation against TradingView logic
"""

import numpy as np
import pandas as pd
import sys
import os

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def test_historical_volatility_basic():
    """Test the Historical Volatility implementation with sample data"""
    
    print("Testing Historical Volatility Implementation...")
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
            vol = 0.5  # Low volatility period
        elif i < 60:
            vol = 2.0  # High volatility period  
        else:
            vol = 1.0  # Medium volatility period
        
        # Random walk with changing volatility
        change = np.random.normal(0, vol)
        new_price = prices[-1] * (1 + change / 100)
        prices.append(max(1, new_price))
    
    close_prices = np.array(prices)
    
    print(f"Generated {n_periods} periods of test data")
    print(f"Price range: {close_prices.min():.2f} - {close_prices.max():.2f}")
    print(f"Price trend: {close_prices[0]:.2f} -> {close_prices[-1]:.2f}")
    print()
    
    # Test with TradingView default parameters
    try:
        print("Testing with TradingView defaults (length=10, annual=365, per=1)...")
        
        hv_result = ta.hv(close_prices)
        
        print(f"  HV calculated successfully")
        print(f"  Result length: {len(hv_result)}")
        print(f"  Non-NaN values: {np.sum(~np.isnan(hv_result))}")
        
        # Find first valid value
        first_valid = np.argmax(~np.isnan(hv_result))
        print(f"  First valid value at index: {first_valid}")
        
        if np.sum(~np.isnan(hv_result)) > 0:
            valid_hv = hv_result[~np.isnan(hv_result)]
            print(f"  HV range: {valid_hv.min():.2f}% - {valid_hv.max():.2f}%")
            print(f"  Average HV: {valid_hv.mean():.2f}%")
            print(f"  Last 5 values: {hv_result[-5:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR: {e}")
        print()
    
    # Test with custom parameters
    try:
        print("Testing with custom parameters (length=20, annual=252, per=1)...")
        
        hv_custom = ta.hv(close_prices, length=20, annual=252, per=1)
        
        print(f"  Custom HV calculated successfully")
        print(f"  Non-NaN values: {np.sum(~np.isnan(hv_custom))}")
        
        if np.sum(~np.isnan(hv_custom)) > 0:
            valid_hv_custom = hv_custom[~np.isnan(hv_custom)]
            print(f"  Custom HV range: {valid_hv_custom.min():.2f}% - {valid_hv_custom.max():.2f}%")
            print(f"  Last 5 values: {hv_custom[-5:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR with custom parameters: {e}")
        print()
    
    # Test weekly timeframe simulation
    try:
        print("Testing weekly timeframe (per=7)...")
        
        hv_weekly = ta.hv(close_prices, length=10, annual=365, per=7)
        
        print(f"  Weekly HV calculated successfully")
        
        if np.sum(~np.isnan(hv_weekly)) > 0:
            valid_hv_weekly = hv_weekly[~np.isnan(hv_weekly)]
            print(f"  Weekly HV range: {valid_hv_weekly.min():.2f}% - {valid_hv_weekly.max():.2f}%")
            print(f"  Last 5 values: {hv_weekly[-5:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR with weekly timeframe: {e}")
        print()

def test_historical_volatility_analysis():
    """Test with realistic market data and analyze volatility regimes"""
    print("Testing with Realistic Market Data...")
    print("=" * 60)
    
    # Create market data with distinct volatility regimes
    n_periods = 200
    np.random.seed(123)
    
    # Simulate different market conditions
    close_prices = []
    base_price = 100
    
    for i in range(n_periods):
        # Define volatility regimes
        if i < 50:
            # Calm market
            daily_vol = 0.008  # ~0.8% daily volatility
            regime = "Calm"
        elif i < 100:
            # Volatile market  
            daily_vol = 0.025  # ~2.5% daily volatility
            regime = "Volatile"
        elif i < 150:
            # Crisis market
            daily_vol = 0.045  # ~4.5% daily volatility  
            regime = "Crisis"
        else:
            # Recovery market
            daily_vol = 0.015  # ~1.5% daily volatility
            regime = "Recovery"
        
        # Generate price change
        change = np.random.normal(0, daily_vol)
        if i == 0:
            price = base_price
        else:
            price = close_prices[-1] * (1 + change)
        
        close_prices.append(max(1, price))
    
    close_prices = np.array(close_prices)
    
    print(f"Market simulation: {n_periods} periods")
    print(f"Regimes: Calm -> Volatile -> Crisis -> Recovery")
    print(f"Price range: {close_prices.min():.2f} - {close_prices.max():.2f}")
    
    # Calculate Historical Volatility
    hv_values = ta.hv(close_prices, length=10, annual=365, per=1)
    
    print(f"\nHistorical Volatility Analysis:")
    
    # Analyze different regimes
    regimes = [
        ("Calm", 0, 50),
        ("Volatile", 50, 100), 
        ("Crisis", 100, 150),
        ("Recovery", 150, 200)
    ]
    
    for regime_name, start, end in regimes:
        regime_hv = hv_values[start:end]
        valid_hv = regime_hv[~np.isnan(regime_hv)]
        
        if len(valid_hv) > 0:
            print(f"  {regime_name} period:")
            print(f"    Average HV: {valid_hv.mean():.2f}%")
            print(f"    HV range: {valid_hv.min():.2f}% - {valid_hv.max():.2f}%")
            print(f"    Std of HV: {valid_hv.std():.2f}%")

def test_with_pandas():
    """Test with pandas data"""
    print("\nTesting with Pandas Series...")
    print("=" * 60)
    
    # Create test data
    n = 50
    np.random.seed(456)
    
    # Generate price series
    prices = [100]
    for i in range(1, n):
        change = np.random.normal(0, 0.02)  # 2% daily volatility
        new_price = prices[-1] * (1 + change)
        prices.append(max(1, new_price))
    
    # Convert to pandas
    close_series = pd.Series(prices)
    
    try:
        hv_pandas = ta.hv(close_series, length=10, annual=365, per=1)
        
        print(f"  Pandas calculation successful!")
        print(f"  Result type: {type(hv_pandas)}")
        print(f"  Valid HV values: {np.sum(~pd.isna(hv_pandas))}/{len(hv_pandas)}")
        
        if np.sum(~pd.isna(hv_pandas)) > 0:
            valid_values = hv_pandas.dropna()
            print(f"  HV range: {valid_values.min():.2f}% - {valid_values.max():.2f}%")
            print(f"  Last 5 values: {hv_pandas.tail().values}")
        
    except Exception as e:
        print(f"  ERROR with pandas: {e}")

def test_parameter_validation():
    """Test parameter validation"""
    print("\nTesting Parameter Validation...")
    print("=" * 60)
    
    # Create minimal test data
    close_prices = np.array([100, 101, 99, 102, 98, 103, 97, 104])
    
    # Test invalid length
    try:
        hv_invalid = ta.hv(close_prices, length=0)
        print("  ERROR: Should have failed with length=0")
    except ValueError as e:
        print(f"  OK: Length validation working: {e}")
    
    # Test invalid annual
    try:
        hv_invalid = ta.hv(close_prices, length=5, annual=-100)
        print("  ERROR: Should have failed with negative annual")
    except ValueError as e:
        print(f"  OK: Annual validation working: {e}")
    
    # Test invalid per
    try:
        hv_invalid = ta.hv(close_prices, length=5, annual=365, per=0)
        print("  ERROR: Should have failed with per=0")
    except ValueError as e:
        print(f"  OK: Per validation working: {e}")
    
    # Test insufficient data
    try:
        short_data = np.array([100, 101])
        hv_short = ta.hv(short_data, length=10)
        print("  ERROR: Should have failed with insufficient data")
    except ValueError as e:
        print(f"  OK: Data length validation working: {e}")

def test_tradingview_comparison():
    """Test specific values that can be manually verified"""
    print("\nTesting TradingView Formula Accuracy...")
    print("=" * 60)
    
    # Use simple test data for manual verification
    close_prices = np.array([100.0, 102.0, 98.0, 105.0, 95.0, 110.0, 90.0, 108.0, 92.0, 106.0, 94.0])
    
    print(f"Test data: {close_prices}")
    
    # Calculate with TradingView parameters
    hv_result = ta.hv(close_prices, length=10, annual=365, per=1)
    
    print(f"Historical Volatility result: {hv_result}")
    
    # Show the calculation for the last value manually
    if len(close_prices) >= 10:
        # Manual calculation for verification
        log_returns = []
        for i in range(1, len(close_prices)):
            log_ret = np.log(close_prices[i] / close_prices[i-1])
            log_returns.append(log_ret)
        
        print(f"\nManual verification for last value:")
        print(f"Log returns: {log_returns}")
        
        if len(log_returns) >= 10:
            last_10_returns = log_returns[-10:]
            mean_return = np.mean(last_10_returns)
            variance = np.sum((np.array(last_10_returns) - mean_return) ** 2) / 10  # Population variance
            stdev = np.sqrt(variance)
            hv_manual = 100 * stdev * np.sqrt(365 / 1)
            
            print(f"Manual calculation: {hv_manual:.6f}")
            print(f"Function result: {hv_result[-1]:.6f}")
            print(f"Difference: {abs(hv_manual - hv_result[-1]):.8f}")

if __name__ == "__main__":
    test_historical_volatility_basic()
    test_historical_volatility_analysis()
    test_with_pandas()
    test_parameter_validation()
    test_tradingview_comparison()