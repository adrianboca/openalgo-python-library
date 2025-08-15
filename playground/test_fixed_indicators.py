#!/usr/bin/env python3
"""
Test the 10 previously failing indicators to verify fixes
"""

import numpy as np
import pandas as pd
import sys
import os
import time

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def generate_test_data(size: int = 100) -> dict:
    """Generate realistic OHLCV data for testing"""
    np.random.seed(42)
    
    base_price = 100.0
    base_volume = 1000000
    
    data = {
        'open': [],
        'high': [],
        'low': [],
        'close': [],
        'volume': []
    }
    
    for i in range(size):
        trend = 0.001 * np.sin(i / 20)
        noise = np.random.normal(0, 0.02)
        
        if i == 0:
            close = base_price
            open_price = base_price
        else:
            daily_return = trend + noise
            open_price = data['close'][-1]
            close = open_price * (1 + daily_return)
        
        # Generate realistic OHLC
        daily_range = abs(np.random.normal(0, 0.015)) * close
        high = close + daily_range * np.random.uniform(0.3, 0.7)
        low = close - daily_range * np.random.uniform(0.3, 0.7)
        
        # Ensure OHLC consistency
        high = max(high, close, open_price)
        low = min(low, close, open_price)
        
        # Generate volume
        volume = int(base_volume * (0.5 + np.random.uniform(0, 1)))
        
        data['open'].append(open_price)
        data['high'].append(high)
        data['low'].append(low)
        data['close'].append(close)
        data['volume'].append(volume)
    
    return {k: np.array(v) for k, v in data.items()}

def test_indicator(name: str, func, data: dict) -> tuple:
    """Test a single indicator"""
    try:
        start_time = time.perf_counter()
        result = func(data)
        end_time = time.perf_counter()
        
        execution_time = (end_time - start_time) * 1000
        
        # Validate result
        if result is None:
            return execution_time, False, "Returned None"
        
        # Handle tuple results
        if isinstance(result, tuple):
            for i, r in enumerate(result):
                if r is None:
                    return execution_time, False, f"Tuple element {i} is None"
                if hasattr(r, '__len__') and len(r) == 0:
                    return execution_time, False, f"Tuple element {i} is empty"
        else:
            if hasattr(result, '__len__') and len(result) == 0:
                return execution_time, False, "Result is empty"
        
        return execution_time, True, "OK"
        
    except Exception as e:
        return 0, False, str(e)

def main():
    """Test the 10 previously failing indicators"""
    
    print("Testing Previously Failing Indicators")
    print("=" * 50)
    
    data = generate_test_data(150)  # Generate enough data for all indicators
    
    # The 10 previously failing indicators with their fixes
    test_indicators = {
        'frama': lambda data: ta.frama(data['high'], data['low'], period=20),
        'chaikin': lambda data: ta.chaikin(data['high'], data['low']),
        'rvol': lambda data: ta.rvol(data['volume']),
        'rvi': lambda data: ta.rvi(data['open'], data['high'], data['low'], data['close']),
        'emv': lambda data: ta.emv(data['high'], data['low'], data['volume']),
        'roc': lambda data: ta.roc(data['close'], length=12),
        'ht': lambda data: ta.ht(data['close'], data['high'], data['low']),
        'cho': lambda data: ta.cho(data['high'], data['low'], data['close'], data['volume']),
        'ckstop': lambda data: ta.ckstop(data['high'], data['low'], data['close']),
        'gator_oscillator': lambda data: ta.gator_oscillator(data['high'], data['low']),
    }
    
    print(f"Generated {len(data['close'])} data points for testing")
    print(f"Testing {len(test_indicators)} indicators...")
    print()
    
    successful_tests = 0
    total_time = 0
    
    for i, (name, func) in enumerate(test_indicators.items(), 1):
        print(f"[{i:2d}/10] Testing {name:<18}", end=" ", flush=True)
        
        exec_time, success, message = test_indicator(name, func, data)
        total_time += exec_time
        
        if success:
            successful_tests += 1
            print(f"{exec_time:8.3f}ms OK  {message}")
        else:
            print(f"          ERROR {message}")
    
    print()
    print("Summary:")
    print(f"  Success Rate: {successful_tests}/10 ({successful_tests/10*100:.1f}%)")
    print(f"  Total Time: {total_time:.3f}ms")
    print(f"  Average Time: {total_time/10:.2f}ms per indicator")
    
    if successful_tests == 10:
        print("\nAll previously failing indicators are now working!")
    else:
        print(f"\n{10-successful_tests} indicators still need attention")

if __name__ == "__main__":
    main()