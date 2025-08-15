#!/usr/bin/env python3
"""
Test LRSLOPE implementation against TradingView logic
"""

import numpy as np
import pandas as pd
import sys
import os

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def tradingview_lrslope_method(data, period, interval=1):
    """
    Calculate slope using TradingView method:
    linear_reg = linreg(close_price, len, 0)
    linear_reg_prev = linreg(close[1], len, 0)
    slope = ((linear_reg - linear_reg_prev) / interval)
    """
    n = len(data)
    slopes = np.full(n, np.nan)
    
    # Calculate linear regression values
    linreg_values = np.full(n, np.nan)
    
    for i in range(period - 1, n):
        # Extract window for linear regression
        y = data[i - period + 1:i + 1]
        x = np.arange(period)
        
        # Calculate linear regression (same as LINREG function)
        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_xy = np.sum(x * y)
        sum_x2 = np.sum(x * x)
        
        denominator = period * sum_x2 - sum_x * sum_x
        if denominator != 0:
            slope_val = (period * sum_xy - sum_x * sum_y) / denominator
            intercept = (sum_y - slope_val * sum_x) / period
            
            # Value at the end of the period
            linreg_values[i] = slope_val * (period - 1) + intercept
        else:
            linreg_values[i] = y[-1]
    
    # Calculate slope as difference between consecutive linreg values
    for i in range(1, n):
        if not np.isnan(linreg_values[i]) and not np.isnan(linreg_values[i-1]):
            slopes[i] = (linreg_values[i] - linreg_values[i-1]) / interval
    
    return slopes, linreg_values

def test_lrslope_comparison():
    """Test both methods and compare results"""
    
    print("Testing LRSLOPE: Current vs TradingView Method")
    print("=" * 60)
    
    # Create test data
    np.random.seed(42)
    n_periods = 50
    
    # Generate trending price data
    base_price = 100
    trend = 0.002  # 0.2% trend per period
    noise = 0.01   # 1% noise
    
    data = []
    for i in range(n_periods):
        if i == 0:
            price = base_price
        else:
            change = trend + np.random.normal(0, noise)
            price = data[-1] * (1 + change)
        data.append(price)
    
    close_data = np.array(data)
    period = 14
    
    print(f"Test data: {n_periods} periods")
    print(f"Price range: {close_data.min():.2f} - {close_data.max():.2f}")
    print(f"Price trend: {close_data[0]:.2f} -> {close_data[-1]:.2f}")
    print(f"Period: {period}")
    print()
    
    # Method 1: Current implementation
    current_slope = ta.lrslope(close_data, period)
    
    # Method 2: TradingView method
    tv_slope, linreg_values = tradingview_lrslope_method(close_data, period)
    
    # Compare results
    print("Comparison of Methods:")
    print("-" * 40)
    
    # Find overlapping valid values
    valid_mask = ~(np.isnan(current_slope) | np.isnan(tv_slope))
    valid_indices = np.where(valid_mask)[0]
    
    if len(valid_indices) > 0:
        current_valid = current_slope[valid_mask]
        tv_valid = tv_slope[valid_mask]
        
        print(f"Valid comparison points: {len(valid_indices)}")
        print(f"Current method range: {current_valid.min():.6f} to {current_valid.max():.6f}")
        print(f"TradingView method range: {tv_valid.min():.6f} to {tv_valid.max():.6f}")
        print()
        
        # Show first few values
        print("First 10 comparison values:")
        print("Index  Current     TradingView   Difference")
        print("-" * 50)
        for i in range(min(10, len(valid_indices))):
            idx = valid_indices[i]
            curr_val = current_slope[idx]
            tv_val = tv_slope[idx]
            diff = curr_val - tv_val
            print(f"{idx:5d}  {curr_val:10.6f}  {tv_val:11.6f}  {diff:10.6f}")
        
        print()
        
        # Statistical comparison
        correlation = np.corrcoef(current_valid, tv_valid)[0, 1]
        mean_diff = np.mean(current_valid - tv_valid)
        max_diff = np.max(np.abs(current_valid - tv_valid))
        
        print(f"Statistical Comparison:")
        print(f"  Correlation: {correlation:.6f}")
        print(f"  Mean difference: {mean_diff:.6f}")
        print(f"  Max absolute difference: {max_diff:.6f}")
        
        # Check if they're essentially the same (within small tolerance)
        if correlation > 0.999 and max_diff < 1e-10:
            print("  OK: Methods are mathematically equivalent")
        elif correlation > 0.99:
            print("  ~: Methods are highly correlated (minor scaling difference)")
        else:
            print("  X: Methods show significant differences")
        
        print()

def test_lrslope_with_different_periods():
    """Test with different periods to match TradingView defaults"""
    
    print("Testing with TradingView Default Period (100)")
    print("=" * 60)
    
    # Create longer test data
    np.random.seed(123)
    n_periods = 150
    
    # Generate data with clear trend
    base_price = 100
    data = [base_price]
    
    for i in range(1, n_periods):
        # Create different trend phases
        if i < 50:
            trend = 0.001  # Slight uptrend
        elif i < 100:
            trend = -0.0005  # Slight downtrend  
        else:
            trend = 0.002  # Stronger uptrend
        
        noise = np.random.normal(0, 0.015)
        new_price = data[-1] * (1 + trend + noise)
        data.append(new_price)
    
    close_data = np.array(data)
    
    # Test with TradingView default period
    period_tv = 100
    period_current = 14
    
    print(f"Data length: {len(close_data)}")
    print(f"TradingView period: {period_tv}")
    print(f"Current default period: {period_current}")
    print()
    
    # Calculate with both periods
    slope_tv_period = ta.lrslope(close_data, period_tv)
    slope_current_period = ta.lrslope(close_data, period_current)
    
    # Compare behavior
    valid_tv = slope_tv_period[~np.isnan(slope_tv_period)]
    valid_current = slope_current_period[~np.isnan(slope_current_period)]
    
    print("Period Comparison:")
    print(f"  Period {period_tv}: {len(valid_tv)} valid values, range {valid_tv.min():.6f} to {valid_tv.max():.6f}")
    print(f"  Period {period_current}: {len(valid_current)} valid values, range {valid_current.min():.6f} to {valid_current.max():.6f}")
    print()
    
    # Show last 5 values for each
    print("Last 5 values:")
    print(f"  Period {period_tv}: {slope_tv_period[-5:]}")
    print(f"  Period {period_current}: {slope_current_period[-5:]}")

def test_manual_calculation():
    """Manual calculation to verify correctness"""
    
    print("Manual Calculation Verification")
    print("=" * 60)
    
    # Simple test data
    data = np.array([100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0, 96.0, 105.0])
    period = 5
    
    print(f"Test data: {data}")
    print(f"Period: {period}")
    print()
    
    # Calculate using our function
    result = ta.lrslope(data, period)
    
    print("Function result:")
    print(f"  LRSLOPE: {result}")
    print()
    
    # Manual calculation for last value
    print("Manual calculation for last window:")
    y = data[-period:]  # Last 5 values
    x = np.arange(period)  # [0, 1, 2, 3, 4]
    
    print(f"  x values: {x}")
    print(f"  y values: {y}")
    
    # Calculate slope manually
    n = period
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x * x)
    
    print(f"  sum_x = {sum_x}")
    print(f"  sum_y = {sum_y}")
    print(f"  sum_xy = {sum_xy}")
    print(f"  sum_x2 = {sum_x2}")
    
    denominator = n * sum_x2 - sum_x * sum_x
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    
    print(f"  denominator = {denominator}")
    print(f"  manual slope = {slope}")
    print(f"  function slope = {result[-1]}")
    print(f"  difference = {abs(slope - result[-1])}")

if __name__ == "__main__":
    test_lrslope_comparison()
    test_lrslope_with_different_periods()
    test_manual_calculation()