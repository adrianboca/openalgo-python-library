#!/usr/bin/env python3
"""
Test Ichimoku implementation against TradingView logic
"""

import numpy as np
import pandas as pd
import sys
import os

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def test_ichimoku_basic():
    """Test the Ichimoku implementation with sample data"""
    
    print("Testing Ichimoku Cloud Implementation...")
    print("=" * 60)
    
    # Create sample OHLC data with trending patterns
    np.random.seed(42)
    n_periods = 100
    
    # Generate realistic OHLC data
    close_prices = []
    high_prices = []
    low_prices = []
    
    base_price = 100
    
    for i in range(n_periods):
        # Create uptrend with some volatility
        if i < 50:
            trend = 0.02  # Uptrend
        else:
            trend = -0.01  # Downtrend
        
        # Random daily change
        change = np.random.normal(trend, 0.015)
        
        if i == 0:
            close = base_price
        else:
            close = close_prices[-1] * (1 + change)
        
        # Generate realistic OHLC
        daily_range = abs(np.random.normal(0, 0.01)) * close
        high = close + daily_range * np.random.uniform(0.3, 0.7)
        low = close - daily_range * np.random.uniform(0.3, 0.7)
        
        close_prices.append(close)
        high_prices.append(high)
        low_prices.append(low)
    
    high_data = np.array(high_prices)
    low_data = np.array(low_prices)
    close_data = np.array(close_prices)
    
    print(f"Generated {n_periods} periods of OHLC data")
    print(f"Price range: {close_data.min():.2f} - {close_data.max():.2f}")
    print(f"Price trend: {close_data[0]:.2f} -> {close_data[-1]:.2f}")
    print()
    
    # Test with TradingView default parameters
    try:
        print("Testing with TradingView defaults...")
        print("conversionPeriods=9, basePeriods=26, laggingSpan2Periods=52, displacement=26")
        
        conversion_line, base_line, leading_span_a, leading_span_b, lagging_span = ta.ichimoku(
            high_data, low_data, close_data
        )
        
        print(f"  Ichimoku calculated successfully")
        print(f"  Result length: {len(conversion_line)}")
        
        # Analyze each component
        components = [
            ("Conversion Line", conversion_line),
            ("Base Line", base_line),
            ("Leading Span A", leading_span_a),
            ("Leading Span B", leading_span_b),
            ("Lagging Span", lagging_span)
        ]
        
        for name, component in components:
            valid_count = np.sum(~np.isnan(component))
            print(f"  {name}: {valid_count} valid values")
            
            if valid_count > 0:
                valid_data = component[~np.isnan(component)]
                print(f"    Range: {valid_data.min():.2f} - {valid_data.max():.2f}")
                print(f"    Last 3 values: {component[-3:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR: {e}")
        print()

def test_ichimoku_custom_params():
    """Test with custom parameters"""
    print("Testing with Custom Parameters...")
    print("=" * 60)
    
    # Create simple test data
    n = 60
    high_data = np.linspace(100, 120, n) + np.random.normal(0, 1, n)
    low_data = high_data - np.random.uniform(1, 3, n)
    close_data = (high_data + low_data) / 2 + np.random.normal(0, 0.5, n)
    
    print(f"Test data: {n} periods")
    
    # Test different parameter combinations
    test_cases = [
        {"conversion_periods": 5, "base_periods": 13, "lagging_span2_periods": 26, "displacement": 13},
        {"conversion_periods": 12, "base_periods": 24, "lagging_span2_periods": 48, "displacement": 24},
        {"conversion_periods": 9, "base_periods": 26, "lagging_span2_periods": 52, "displacement": 0},  # No displacement
    ]
    
    for i, params in enumerate(test_cases, 1):
        try:
            print(f"Test case {i}: {params}")
            
            result = ta.ichimoku(high_data, low_data, close_data, **params)
            conversion_line, base_line, leading_span_a, leading_span_b, lagging_span = result
            
            # Check for valid data
            valid_counts = [np.sum(~np.isnan(comp)) for comp in result]
            print(f"  Valid values: {valid_counts}")
            
            # Check displacement effect
            if params["displacement"] > 0:
                displacement = params["displacement"]
                print(f"  Displacement effect (displacement={displacement}):")
                print(f"    Leading Span A first valid at: {np.argmax(~np.isnan(leading_span_a))}")
                print(f"    Leading Span B first valid at: {np.argmax(~np.isnan(leading_span_b))}")
                print(f"    Lagging Span last valid at: {len(lagging_span) - np.argmax(~np.isnan(lagging_span[::-1])) - 1}")
            
            print()
            
        except Exception as e:
            print(f"  ERROR in test case {i}: {e}")
            print()

def test_with_pandas():
    """Test with pandas data"""
    print("Testing with Pandas Series...")
    print("=" * 60)
    
    # Create pandas DataFrame
    n = 50
    np.random.seed(123)
    
    data = {
        'high': np.random.uniform(100, 120, n),
        'low': np.random.uniform(80, 100, n),
        'close': np.random.uniform(90, 110, n)
    }
    
    # Ensure high >= low
    data['high'] = np.maximum(data['high'], data['low'] + 1)
    data['close'] = np.clip(data['close'], data['low'], data['high'])
    
    df = pd.DataFrame(data)
    
    try:
        result = ta.ichimoku(df['high'], df['low'], df['close'])
        conversion_line, base_line, leading_span_a, leading_span_b, lagging_span = result
        
        print(f"  Pandas calculation successful!")
        print(f"  Result types: {[type(comp).__name__ for comp in result]}")
        
        # Check if results are pandas Series
        if all(isinstance(comp, pd.Series) for comp in result):
            print(f"  Results are pandas Series with proper index")
            print(f"  Index matches input: {all(comp.index.equals(df.index) for comp in result)}")
        
        # Show sample values
        print(f"  Sample values (last 5):")
        for name, comp in zip(['Conversion', 'Base', 'Lead A', 'Lead B', 'Lagging'], result):
            if isinstance(comp, pd.Series):
                print(f"    {name}: {comp.tail().values}")
            else:
                print(f"    {name}: {comp[-5:]}")
        
        print()
        
    except Exception as e:
        print(f"  ERROR with pandas: {e}")
        print()

def test_parameter_validation():
    """Test parameter validation"""
    print("Testing Parameter Validation...")
    print("=" * 60)
    
    # Create minimal test data
    high_data = np.array([102, 103, 101, 104, 100, 105])
    low_data = np.array([98, 99, 97, 100, 96, 101])
    close_data = np.array([100, 101, 99, 102, 98, 103])
    
    # Test invalid parameters
    test_cases = [
        {"conversion_periods": 0, "error_msg": "conversion_periods must be positive"},
        {"base_periods": -5, "error_msg": "base_periods must be positive"},
        {"lagging_span2_periods": 0, "error_msg": "lagging_span2_periods must be positive"},
    ]
    
    for case in test_cases:
        try:
            params = {"conversion_periods": 9, "base_periods": 26, "lagging_span2_periods": 52, "displacement": 26}
            params.update({k: v for k, v in case.items() if k != "error_msg"})
            
            result = ta.ichimoku(high_data, low_data, close_data, **params)
            print(f"  ERROR: Should have failed with {case['error_msg']}")
            
        except ValueError as e:
            print(f"  OK: Parameter validation working: {e}")
        except Exception as e:
            print(f"  Unexpected error: {e}")

def test_tradingview_formula():
    """Test specific calculations that match TradingView logic"""
    print("Testing TradingView Formula Logic...")
    print("=" * 60)
    
    # Create simple test data for manual verification
    high_data = np.array([105, 107, 103, 109, 101, 112, 98, 115, 95, 118, 92, 121, 89, 124])
    low_data = np.array([95, 97, 93, 99, 91, 102, 88, 105, 85, 108, 82, 111, 79, 114])
    close_data = np.array([100, 102, 98, 104, 96, 107, 93, 110, 90, 113, 87, 116, 84, 119])
    
    print(f"Test data length: {len(close_data)}")
    print(f"High: {high_data}")
    print(f"Low: {low_data}")
    print(f"Close: {close_data}")
    print()
    
    # Calculate Ichimoku with small periods for verification
    conversion_line, base_line, leading_span_a, leading_span_b, lagging_span = ta.ichimoku(
        high_data, low_data, close_data, 
        conversion_periods=3, base_periods=6, lagging_span2_periods=9, displacement=3
    )
    
    print("TradingView Logic Verification:")
    print("donchian(len) => math.avg(ta.lowest(len), ta.highest(len))")
    print()
    
    # Manual calculation for last few values
    n = len(high_data)
    if n >= 9:
        # Conversion line (period=3): avg of highest(3) and lowest(3)
        for i in range(max(3, 6, 9)-1, min(n, max(3, 6, 9)+3)):
            if i >= 2:  # conversion period - 1
                conv_high = np.max(high_data[i-2:i+1])
                conv_low = np.min(low_data[i-2:i+1])
                manual_conv = (conv_high + conv_low) / 2.0
                print(f"  Period {i}: Conversion manual={manual_conv:.2f}, calculated={conversion_line[i]:.2f}")
            
            if i >= 5:  # base period - 1
                base_high = np.max(high_data[i-5:i+1])
                base_low = np.min(low_data[i-5:i+1])
                manual_base = (base_high + base_low) / 2.0
                print(f"  Period {i}: Base manual={manual_base:.2f}, calculated={base_line[i]:.2f}")
    
    print()
    print("Results:")
    print(f"  Conversion Line: {conversion_line}")
    print(f"  Base Line: {base_line}")
    print(f"  Leading Span A: {leading_span_a}")
    print(f"  Leading Span B: {leading_span_b}")
    print(f"  Lagging Span: {lagging_span}")

if __name__ == "__main__":
    test_ichimoku_basic()
    test_ichimoku_custom_params()
    test_with_pandas()
    test_parameter_validation()
    test_tradingview_formula()