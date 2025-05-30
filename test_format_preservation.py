#!/usr/bin/env python3
"""
Test script to verify format preservation in OpenAlgo indicators
"""

import numpy as np
import pandas as pd
import sys
import os

# Add the openalgo module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from openalgo import ta

def test_format_preservation():
    """Test that indicators return the same format as their input"""
    
    # Test data
    np.random.seed(42)
    data_length = 100
    close_list = [100 + i + np.random.randn() for i in range(data_length)]
    
    # Convert to different formats
    close_numpy = np.array(close_list)
    dates = pd.date_range('2024-01-01', periods=data_length)
    close_pandas = pd.Series(close_list, index=dates)
    
    print("Testing Format Preservation in OpenAlgo Indicators")
    print("=" * 50)
    
    # Test 1: NumPy input
    print("\n1. Testing NumPy array input:")
    sma_numpy = ta.sma(close_numpy, 20)
    ema_numpy = ta.ema(close_numpy, 20)
    rsi_numpy = ta.rsi(close_numpy, 14)
    
    print(f"   Input type: {type(close_numpy)}")
    print(f"   SMA output type: {type(sma_numpy)}")
    print(f"   EMA output type: {type(ema_numpy)}")
    print(f"   RSI output type: {type(rsi_numpy)}")
    
    assert isinstance(sma_numpy, np.ndarray), "SMA should return numpy array"
    assert isinstance(ema_numpy, np.ndarray), "EMA should return numpy array"
    assert isinstance(rsi_numpy, np.ndarray), "RSI should return numpy array"
    print("   ✓ All outputs are numpy arrays")
    
    # Test 2: Pandas input
    print("\n2. Testing Pandas Series input:")
    sma_pandas = ta.sma(close_pandas, 20)
    ema_pandas = ta.ema(close_pandas, 20)
    rsi_pandas = ta.rsi(close_pandas, 14)
    
    print(f"   Input type: {type(close_pandas)}")
    print(f"   SMA output type: {type(sma_pandas)}")
    print(f"   EMA output type: {type(ema_pandas)}")
    print(f"   RSI output type: {type(rsi_pandas)}")
    
    assert isinstance(sma_pandas, pd.Series), "SMA should return pandas Series"
    assert isinstance(ema_pandas, pd.Series), "EMA should return pandas Series"
    assert isinstance(rsi_pandas, pd.Series), "RSI should return pandas Series"
    print("   ✓ All outputs are pandas Series")
    
    # Test 3: Index preservation
    print("\n3. Testing index preservation:")
    print(f"   Original index: {close_pandas.index[:5]}")
    print(f"   SMA index: {sma_pandas.index[:5]}")
    
    assert sma_pandas.index.equals(close_pandas.index), "Index should be preserved"
    assert ema_pandas.index.equals(close_pandas.index), "Index should be preserved"
    assert rsi_pandas.index.equals(close_pandas.index), "Index should be preserved"
    print("   ✓ Index preserved correctly")
    
    # Test 4: List input
    print("\n4. Testing Python list input:")
    sma_list = ta.sma(close_list, 20)
    ema_list = ta.ema(close_list, 20)
    rsi_list = ta.rsi(close_list, 14)
    
    print(f"   Input type: {type(close_list)}")
    print(f"   SMA output type: {type(sma_list)}")
    print(f"   EMA output type: {type(ema_list)}")
    print(f"   RSI output type: {type(rsi_list)}")
    
    assert isinstance(sma_list, np.ndarray), "SMA should return numpy array for list input"
    assert isinstance(ema_list, np.ndarray), "EMA should return numpy array for list input"
    assert isinstance(rsi_list, np.ndarray), "RSI should return numpy array for list input"
    print("   ✓ All outputs are numpy arrays")
    
    # Test 5: Multi-output indicators
    print("\n5. Testing multi-output indicators:")
    
    # Generate OHLCV data
    high_numpy = close_numpy + np.random.uniform(0, 2, len(close_numpy))
    low_numpy = close_numpy - np.random.uniform(0, 2, len(close_numpy))
    high_pandas = pd.Series(high_numpy, index=dates)
    low_pandas = pd.Series(low_numpy, index=dates)
    
    # Test Supertrend with numpy
    st_numpy, dir_numpy = ta.supertrend(high_numpy, low_numpy, close_numpy, 10, 3)
    print(f"   NumPy Supertrend types: {type(st_numpy)}, {type(dir_numpy)}")
    assert isinstance(st_numpy, np.ndarray) and isinstance(dir_numpy, np.ndarray)
    
    # Test Supertrend with pandas
    st_pandas, dir_pandas = ta.supertrend(high_pandas, low_pandas, close_pandas, 10, 3)
    print(f"   Pandas Supertrend types: {type(st_pandas)}, {type(dir_pandas)}")
    assert isinstance(st_pandas, pd.Series) and isinstance(dir_pandas, pd.Series)
    assert st_pandas.index.equals(close_pandas.index)
    print("   ✓ Multi-output format preservation works")
    
    # Test 6: Value accuracy
    print("\n6. Testing value accuracy across formats:")
    
    # Compare values (should be identical regardless of format)
    np.testing.assert_array_almost_equal(
        sma_numpy[~np.isnan(sma_numpy)], 
        sma_pandas.dropna().values, 
        decimal=10
    )
    print("   ✓ SMA values identical across formats")
    
    np.testing.assert_array_almost_equal(
        rsi_numpy[~np.isnan(rsi_numpy)], 
        rsi_pandas.dropna().values, 
        decimal=10
    )
    print("   ✓ RSI values identical across formats")
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED! Format preservation is working correctly.")
    print("\nKey benefits:")
    print("- Pandas input → Pandas output (with preserved index)")
    print("- NumPy input → NumPy output")
    print("- List input → NumPy output")
    print("- Multi-output indicators preserve format")
    print("- Values are identical regardless of input format")

if __name__ == "__main__":
    test_format_preservation()