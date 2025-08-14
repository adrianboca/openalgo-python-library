#!/usr/bin/env python3
"""
Test script to verify the 5 fixed Numba compilation issues
"""

import numpy as np
import sys

# Add the openalgo package to path
sys.path.insert(0, '/Users/openalgo/openalgo-python-library/openalgo-python-library')

try:
    from openalgo import ta
    print("✓ Successfully imported OpenAlgo library")
except ImportError as e:
    print(f"✗ Failed to import OpenAlgo library: {e}")
    sys.exit(1)

def test_indicator(name, test_func):
    """Test a single indicator"""
    try:
        result = test_func()
        if result is not None:
            print(f"✓ {name} - WORKING")
            return True
        else:
            print(f"✗ {name} - FAILED (returned None)")
            return False
    except Exception as e:
        print(f"✗ {name} - FAILED: {str(e)}")
        return False

# Generate test data
np.random.seed(42)
length = 100

# Price data
base_price = 100
price_changes = np.random.randn(length) * 0.02
close = base_price * np.exp(np.cumsum(price_changes))
open_prices = close * (1 + np.random.randn(length) * 0.001)
high = np.maximum(open_prices, close) * (1 + np.abs(np.random.randn(length)) * 0.01)
low = np.minimum(open_prices, close) * (1 - np.abs(np.random.randn(length)) * 0.01)
volume = np.random.randint(1000, 10000, length).astype(float)
typical_price = (high + low + close) / 3

print("\n" + "="*50)
print("TESTING 5 FIXED INDICATORS")
print("="*50)

passed = 0
failed = 0

# Test 1: VIDYA (Fixed Numba self-reference)
if test_indicator("vidya", lambda: ta.vidya(close, 14, 0.2)):
    passed += 1
else:
    failed += 1

# Test 2: RVOL (Fixed parameter signature)
if test_indicator("rvol", lambda: ta.rvol(close, 10, 14)):
    passed += 1
else:
    failed += 1

# Test 3: Chandelier Exit (Fixed Numba self-reference)
if test_indicator("chandelier_exit", lambda: ta.chandelier_exit(high, low, close, 22, 3.0)):
    passed += 1
else:
    failed += 1

# Test 4: StochRSI (Fixed Numba self-reference)
if test_indicator("stochrsi", lambda: ta.stochrsi(close, 14, 14, 3, 3)):
    passed += 1
else:
    failed += 1

# Test 5: CHOP (Fixed Numba self-reference)
if test_indicator("chop", lambda: ta.chop(high, low, close, 14)):
    passed += 1
else:
    failed += 1

print("\n" + "="*50)
print("RESULTS")
print("="*50)
print(f"Passed: {passed} ✓")
print(f"Failed: {failed} ✗")
print(f"Success Rate: {(passed / 5 * 100):.1f}%")

if failed == 0:
    print("\n🎉 ALL FIXES SUCCESSFUL!")
else:
    print(f"\n⚠️  {failed} indicators still have issues")

sys.exit(0 if failed == 0 else 1)