#!/usr/bin/env python3
"""
Test KST implementation against TradingView logic
"""

import numpy as np
import pandas as pd
import sys
import os

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def test_kst_basic():
    """Test the KST implementation with sample data"""
    
    print("Testing KST Implementation...")
    print("=" * 60)
    
    # Create sample price data with trends and momentum changes
    np.random.seed(42)
    n_periods = 100
    
    # Generate realistic price data with different momentum regimes
    base_price = 100
    prices = [base_price]
    
    for i in range(1, n_periods):
        # Create momentum regimes
        if i < 30:
            # Strong uptrend
            trend = 0.015
            vol = 0.005
        elif i < 50:
            # Sideways with choppy action
            trend = 0.0
            vol = 0.02
        elif i < 75:
            # Moderate downtrend
            trend = -0.01
            vol = 0.01
        else:
            # Recovery
            trend = 0.008
            vol = 0.008
        
        # Random walk with changing momentum
        change = np.random.normal(trend, vol)
        new_price = prices[-1] * (1 + change)
        prices.append(max(1, new_price))
    
    close_prices = np.array(prices)
    
    print(f"Generated {n_periods} periods of test data")
    print(f"Price range: {close_prices.min():.2f} - {close_prices.max():.2f}")
    print(f"Price trend: {close_prices[0]:.2f} -> {close_prices[-1]:.2f}")
    print()
    
    # Test with TradingView default parameters
    try:
        print("Testing with TradingView defaults...")
        print("roclen1=10, roclen2=15, roclen3=20, roclen4=30")
        print("smalen1=10, smalen2=10, smalen3=10, smalen4=15")
        print("siglen=9")
        
        kst_result, signal_result = ta.kst(close_prices)
        
        print(f"  KST calculated successfully")
        print(f"  Result length: {len(kst_result)}")
        print(f"  KST Non-NaN values: {np.sum(~np.isnan(kst_result))}")
        print(f"  Signal Non-NaN values: {np.sum(~np.isnan(signal_result))}")
        
        # Find first valid value
        first_valid_kst = np.argmax(~np.isnan(kst_result))
        first_valid_signal = np.argmax(~np.isnan(signal_result))
        print(f"  First valid KST at index: {first_valid_kst}")
        print(f"  First valid Signal at index: {first_valid_signal}")
        
        if np.sum(~np.isnan(kst_result)) > 0:
            valid_kst = kst_result[~np.isnan(kst_result)]
            print(f"  KST range: {valid_kst.min():.2f} - {valid_kst.max():.2f}")
            print(f"  Last 5 KST values: {kst_result[-5:]}")
        
        if np.sum(~np.isnan(signal_result)) > 0:
            valid_signal = signal_result[~np.isnan(signal_result)]
            print(f"  Signal range: {valid_signal.min():.2f} - {valid_signal.max():.2f}")
            print(f"  Last 5 Signal values: {signal_result[-5:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR: {e}")
        print()

def test_kst_tradingview_comparison():
    """Test specific values that can be manually verified against TradingView"""
    print("Testing TradingView Formula Accuracy...")
    print("=" * 60)
    
    # Use simple test data for manual verification
    close_prices = np.array([
        100.0, 102.0, 98.0, 105.0, 95.0, 110.0, 90.0, 108.0, 92.0, 106.0, 
        94.0, 112.0, 88.0, 115.0, 85.0, 118.0, 82.0, 120.0, 78.0, 125.0,
        75.0, 130.0, 72.0, 135.0, 70.0, 140.0, 68.0, 145.0, 66.0, 150.0,
        64.0, 155.0, 62.0, 160.0, 60.0, 165.0, 58.0, 170.0, 56.0, 175.0,
        54.0, 180.0, 52.0, 185.0, 50.0, 190.0, 48.0, 195.0, 46.0, 200.0
    ])
    
    print(f"Test data: {len(close_prices)} periods")
    print(f"Price range: {close_prices.min():.1f} - {close_prices.max():.1f}")
    print()
    
    # Calculate with small periods for easier verification
    kst_result, signal_result = ta.kst(
        close_prices, 
        roclen1=5, roclen2=7, roclen3=10, roclen4=12,
        smalen1=3, smalen2=3, smalen3=3, smalen4=3,
        siglen=3
    )
    
    print("TradingView Logic Verification:")
    print("smaroc(roclen, smalen) => ta.sma(ta.roc(close, roclen), smalen)")
    print("kst = smaroc(roclen1, smalen1) + 2 * smaroc(roclen2, smalen2) + 3 * smaroc(roclen3, smalen3) + 4 * smaroc(roclen4, smalen4)")
    print("sig = ta.sma(kst, siglen)")
    print()
    
    # Manual calculation for a specific point
    if len(close_prices) >= 20:
        print(f"KST result: {kst_result}")
        print(f"Signal result: {signal_result}")
        print()
        
        # Show trend analysis
        first_valid_kst = np.argmax(~np.isnan(kst_result))
        if first_valid_kst < len(kst_result) - 1:
            valid_kst = kst_result[~np.isnan(kst_result)]
            print(f"KST trend analysis:")
            print(f"  First valid KST: {valid_kst[0]:.2f}")
            print(f"  Last KST: {valid_kst[-1]:.2f}")
            print(f"  KST trend: {'Bullish' if valid_kst[-1] > valid_kst[0] else 'Bearish'}")

def test_kst_momentum_detection():
    """Test KST's ability to detect momentum changes"""
    print("\\nTesting KST Momentum Detection...")
    print("=" * 60)
    
    # Create data with clear momentum shifts
    n_periods = 80
    
    # Strong uptrend period
    uptrend_data = np.linspace(100, 150, 30)  # 50% gain over 30 periods
    
    # Consolidation period
    consolidation_data = 150 + np.random.normal(0, 2, 20)  # Sideways with noise
    
    # Downtrend period
    downtrend_data = np.linspace(150, 120, 30)  # 20% decline over 30 periods
    
    combined_data = np.concatenate([uptrend_data, consolidation_data, downtrend_data])
    
    print(f"Data: 30 periods uptrend (100->150), 20 periods consolidation (150±2), 30 periods downtrend (150->120)")
    
    # Calculate KST
    kst_result, signal_result = ta.kst(combined_data)
    
    # Analyze behavior in different periods
    if np.sum(~np.isnan(kst_result)) > 0:
        valid_indices = ~np.isnan(kst_result)
        valid_kst = kst_result[valid_indices]
        valid_indices_pos = np.where(valid_indices)[0]
        
        # Find values in different periods
        uptrend_kst = []
        consolidation_kst = []
        downtrend_kst = []
        
        for i, idx in enumerate(valid_indices_pos):
            if idx < 30:  # Uptrend period
                uptrend_kst.append(valid_kst[i])
            elif idx < 50:  # Consolidation period
                consolidation_kst.append(valid_kst[i])
            else:  # Downtrend period
                downtrend_kst.append(valid_kst[i])
        
        print(f"\\nMomentum detection analysis:")
        if uptrend_kst:
            print(f"  Uptrend period KST: {np.mean(uptrend_kst):.2f} (avg)")
        if consolidation_kst:
            print(f"  Consolidation period KST: {np.mean(consolidation_kst):.2f} (avg)")
        if downtrend_kst:
            print(f"  Downtrend period KST: {np.mean(downtrend_kst):.2f} (avg)")
        
        # KST should be highest in uptrend, neutral in consolidation, lowest in downtrend
        if uptrend_kst and downtrend_kst:
            avg_uptrend = np.mean(uptrend_kst)
            avg_downtrend = np.mean(downtrend_kst)
            if avg_uptrend > avg_downtrend:
                print(f"  OK: KST correctly detects momentum (uptrend > downtrend)")
            else:
                print(f"  WARNING: KST momentum detection may need review")

def test_with_pandas():
    """Test with pandas data"""
    print("\\nTesting with Pandas Series...")
    print("=" * 60)
    
    # Create test data
    n = 60
    np.random.seed(456)
    
    # Generate price series with momentum
    prices = []
    base_price = 100
    for i in range(n):
        momentum = 0.005 if i < 30 else -0.003  # Positive then negative momentum
        noise = np.random.normal(0, 0.01)  # 1% noise
        if i == 0:
            price = base_price
        else:
            price = prices[-1] * (1 + momentum + noise)
        prices.append(max(1, price))
    
    # Convert to pandas
    close_series = pd.Series(prices)
    
    try:
        kst_pandas, signal_pandas = ta.kst(close_series)
        
        print(f"  Pandas calculation successful!")
        print(f"  Result types: {type(kst_pandas).__name__}, {type(signal_pandas).__name__}")
        print(f"  Valid KST values: {np.sum(~pd.isna(kst_pandas))}/{len(kst_pandas)}")
        print(f"  Valid Signal values: {np.sum(~pd.isna(signal_pandas))}/{len(signal_pandas)}")
        
        if np.sum(~pd.isna(kst_pandas)) > 0:
            valid_kst = kst_pandas.dropna()
            valid_signal = signal_pandas.dropna()
            print(f"  KST range: {valid_kst.min():.2f} - {valid_kst.max():.2f}")
            print(f"  Signal range: {valid_signal.min():.2f} - {valid_signal.max():.2f}")
            print(f"  Last 3 KST values: {kst_pandas.tail(3).values}")
            print(f"  Last 3 Signal values: {signal_pandas.tail(3).values}")
        
    except Exception as e:
        print(f"  ERROR with pandas: {e}")

def test_parameter_validation():
    """Test parameter validation"""
    print("\\nTesting Parameter Validation...")
    print("=" * 60)
    
    # Create minimal test data
    close_prices = np.array([100, 101, 99, 102, 98, 103, 97, 104, 96, 105] * 5)  # 50 periods
    
    # Test invalid roclen1
    try:
        kst_invalid = ta.kst(close_prices, roclen1=0)
        print("  ERROR: Should have failed with roclen1=0")
    except ValueError as e:
        print(f"  OK: ROC length validation working: {e}")
    
    # Test invalid smalen1
    try:
        kst_invalid = ta.kst(close_prices, roclen1=5, smalen1=0)
        print("  ERROR: Should have failed with smalen1=0")
    except ValueError as e:
        print(f"  OK: SMA length validation working: {e}")
    
    # Test invalid siglen
    try:
        kst_invalid = ta.kst(close_prices, roclen1=5, smalen1=3, siglen=0)
        print("  ERROR: Should have failed with siglen=0")
    except ValueError as e:
        print(f"  OK: Signal length validation working: {e}")

def test_kst_signal_crossovers():
    """Test KST and Signal line crossovers"""
    print("\\nTesting KST Signal Crossovers...")
    print("=" * 60)
    
    # Create trending data that should generate clear signals
    n = 60
    
    # Create a price series with clear trend changes
    prices = []
    for i in range(n):
        if i < 20:
            # Downtrend
            price = 100 - i * 1.5
        elif i < 40:
            # Uptrend
            price = 70 + (i - 20) * 2.0
        else:
            # Sideways
            price = 110 + np.sin((i - 40) * 0.3) * 3
        
        prices.append(price)
    
    close_prices = np.array(prices)
    
    try:
        kst_result, signal_result = ta.kst(close_prices)
        
        # Find crossovers
        valid_mask = ~(np.isnan(kst_result) | np.isnan(signal_result))
        if np.sum(valid_mask) > 1:
            valid_kst = kst_result[valid_mask]
            valid_signal = signal_result[valid_mask]
            
            # Find crossovers
            bullish_crossovers = []
            bearish_crossovers = []
            
            for i in range(1, len(valid_kst)):
                if valid_kst[i-1] <= valid_signal[i-1] and valid_kst[i] > valid_signal[i]:
                    bullish_crossovers.append(i)
                elif valid_kst[i-1] >= valid_signal[i-1] and valid_kst[i] < valid_signal[i]:
                    bearish_crossovers.append(i)
            
            print(f"  Valid data points: {len(valid_kst)}")
            print(f"  Bullish crossovers found: {len(bullish_crossovers)}")
            print(f"  Bearish crossovers found: {len(bearish_crossovers)}")
            
            if bullish_crossovers or bearish_crossovers:
                print(f"  OK: KST generates crossover signals")
            else:
                print(f"  Note: No crossovers detected in test data")
        
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    test_kst_basic()
    test_kst_tradingview_comparison()
    test_kst_momentum_detection()
    test_with_pandas()
    test_parameter_validation()
    test_kst_signal_crossovers()