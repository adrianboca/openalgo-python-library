#!/usr/bin/env python3
"""
Debug KVO implementation
"""

import numpy as np
import sys
import os

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

def debug_kvo_calculation():
    """Debug KVO calculation step by step"""
    
    print("Debugging KVO Calculation...")
    print("=" * 60)
    
    # Simple test data
    high_data = np.array([102.0, 104.0, 101.0, 106.0, 103.0])
    low_data = np.array([98.0, 100.0, 97.0, 102.0, 99.0])
    close_data = np.array([100.0, 102.0, 99.0, 104.0, 101.0])
    volume_data = np.array([1000.0, 1100.0, 900.0, 1200.0, 800.0])
    
    print("Test data:")
    print(f"High:   {high_data}")
    print(f"Low:    {low_data}")
    print(f"Close:  {close_data}")
    print(f"Volume: {volume_data}")
    print()
    
    # Manual calculation
    hlc3 = (high_data + low_data + close_data) / 3.0
    print(f"HLC3:   {hlc3}")
    
    # Manual xTrend calculation
    x_trend = np.zeros(len(close_data))
    x_trend[0] = volume_data[0] * 100.0  # First value positive
    
    for i in range(1, len(hlc3)):
        if hlc3[i] > hlc3[i-1]:
            x_trend[i] = volume_data[i] * 100.0
        else:
            x_trend[i] = -volume_data[i] * 100.0
    
    print(f"xTrend: {x_trend}")
    print()
    
    # Test the function
    try:
        kvo_result, trigger_result = ta.kvo(high_data, low_data, close_data, volume_data, 
                                           trig_len=3, fast_x=5, slow_x=8)
        print(f"KVO result: {kvo_result}")
        print(f"Trigger result: {trigger_result}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_kvo_calculation()