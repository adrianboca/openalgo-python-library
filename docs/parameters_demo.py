#!/usr/bin/env python3
"""
OpenAlgo Technical Indicators - Parameters Demo

This script demonstrates the difference between mandatory and optional parameters
in the OpenAlgo technical indicators library.
"""

import numpy as np
from openalgo import ta

# Generate sample data
np.random.seed(42)
n = 100
close = 100 + np.cumsum(np.random.randn(n) * 0.01)
high = close + np.random.uniform(0, 2, n)
low = close - np.random.uniform(0, 2, n)
volume = np.random.randint(10000, 100000, n)

print("🎯 OpenAlgo Technical Indicators - Parameters Demo")
print("=" * 60)

print("\n📊 MANDATORY vs OPTIONAL Parameters Examples")
print("-" * 50)

# 1. Indicators with ALL mandatory parameters
print("\n🔴 Indicators with ALL MANDATORY parameters:")
print("   (Must provide all parameters)")

try:
    sma_20 = ta.sma(close, 20)
    print(f"✅ ta.sma(close, 20) - SMA: {sma_20[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    obv_values = ta.obv(close, volume)
    print(f"✅ ta.obv(close, volume) - OBV: {obv_values[-1]:,.0f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    true_range = ta.true_range(high, low, close)
    print(f"✅ ta.true_range(high, low, close) - TR: {true_range[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

# 2. Indicators with optional parameters - using defaults
print("\n🟢 Indicators with OPTIONAL parameters (using defaults):")
print("   (Can omit optional parameters)")

try:
    rsi_default = ta.rsi(close)  # Uses default period=14
    print(f"✅ ta.rsi(close) - RSI with default period=14: {rsi_default[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    macd_line, signal_line, histogram = ta.macd(close)  # Uses defaults 12,26,9
    print(f"✅ ta.macd(close) - MACD with defaults (12,26,9): {macd_line[-1]:.4f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    atr_default = ta.atr(high, low, close)  # Uses default period=14
    print(f"✅ ta.atr(high, low, close) - ATR with default period=14: {atr_default[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    bb_upper, bb_middle, bb_lower = ta.bbands(close)  # Uses defaults 20, 2.0
    print(f"✅ ta.bbands(close) - BB with defaults (20, 2.0): {bb_upper[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    supertrend_vals, direction = ta.supertrend(high, low, close)  # Uses defaults 10, 3.0
    print(f"✅ ta.supertrend(high, low, close) - ST with defaults (10, 3.0): {supertrend_vals[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    alma_default = ta.alma(close)  # Uses defaults 21, 0.85, 6.0
    print(f"✅ ta.alma(close) - ALMA with defaults (21, 0.85, 6.0): {alma_default[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

# 3. Same indicators with custom parameters
print("\n🎨 Same indicators with CUSTOM parameters:")
print("   (Overriding defaults with custom values)")

try:
    rsi_custom = ta.rsi(close, 21)  # Custom period
    print(f"✅ ta.rsi(close, 21) - RSI with custom period=21: {rsi_custom[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    macd_line, signal_line, histogram = ta.macd(close, 10, 20, 7)  # Custom periods
    print(f"✅ ta.macd(close, 10, 20, 7) - MACD with custom (10,20,7): {macd_line[-1]:.4f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    atr_custom = ta.atr(high, low, close, 20)  # Custom period
    print(f"✅ ta.atr(high, low, close, 20) - ATR with custom period=20: {atr_custom[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    bb_upper, bb_middle, bb_lower = ta.bbands(close, 14, 1.5)  # Custom parameters
    print(f"✅ ta.bbands(close, 14, 1.5) - BB with custom (14, 1.5): {bb_upper[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    supertrend_vals, direction = ta.supertrend(high, low, close, 7, 2.0)  # Custom parameters
    print(f"✅ ta.supertrend(high, low, close, 7, 2.0) - ST with custom (7, 2.0): {supertrend_vals[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    alma_custom = ta.alma(close, 30, 0.9, 7.0)  # Custom parameters
    print(f"✅ ta.alma(close, 30, 0.9, 7.0) - ALMA with custom (30, 0.9, 7.0): {alma_custom[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

# 4. Partial parameter customization
print("\n🎯 PARTIAL parameter customization:")
print("   (Mix of defaults and custom values)")

try:
    # ALMA with custom period but default offset and sigma
    alma_partial = ta.alma(close, period=30)  # period=30, offset=0.85, sigma=6.0
    print(f"✅ ta.alma(close, period=30) - ALMA: period=30, offset=0.85 (default), sigma=6.0 (default)")
    print(f"   Result: {alma_partial[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    # Keltner Channel with custom EMA period but default ATR and multiplier
    kc_upper, kc_middle, kc_lower = ta.keltner_channel(high, low, close, ema_period=14)
    print(f"✅ ta.keltner_channel(high, low, close, ema_period=14)")
    print(f"   ema_period=14 (custom), atr_period=10 (default), multiplier=2.0 (default)")
    print(f"   Result: {kc_upper[-1]:.2f}")
except Exception as e:
    print(f"❌ Error: {e}")

# 5. Common mistakes
print("\n❌ COMMON MISTAKES:")
print("   (What happens when you forget mandatory parameters)")

print("\n🔴 Trying to call indicators without mandatory parameters:")

try:
    # This will fail - missing required parameters
    wrong_sma = ta.sma(close)  # Missing period parameter
    print(f"ta.sma(close) - This should fail!")
except Exception as e:
    print(f"❌ ta.sma(close) failed as expected: {type(e).__name__}")

try:
    # This will fail - missing required parameters  
    wrong_obv = ta.obv(close)  # Missing volume parameter
    print(f"ta.obv(close) - This should fail!")
except Exception as e:
    print(f"❌ ta.obv(close) failed as expected: {type(e).__name__}")

try:
    # This will fail - missing required parameters
    wrong_stoch = ta.stochastic(high, low)  # Missing close parameter
    print(f"ta.stochastic(high, low) - This should fail!")
except Exception as e:
    print(f"❌ ta.stochastic(high, low) failed as expected: {type(e).__name__}")

print("\n📋 SUMMARY:")
print("=" * 60)
print("🔴 MANDATORY parameters: Must always be provided")
print("🟢 OPTIONAL parameters: Have sensible defaults, can be omitted")
print("🎨 CUSTOM parameters: Can override defaults for fine-tuning")
print("🎯 PARTIAL customization: Mix defaults with custom values")
print("\n💡 TIP: Start with defaults, then customize as needed!")
print("\n📚 See PARAMETERS_REFERENCE.md for complete parameter details")

if __name__ == "__main__":
    print("\n✅ Demo completed successfully!")
    print("🔗 For more details, check the documentation:")
    print("   - PARAMETERS_REFERENCE.md - Complete parameter specifications")
    print("   - INDICATORS_QUICK_REFERENCE.md - Quick lookup tables")
    print("   - TECHNICAL_INDICATORS_GUIDE.md - Detailed explanations")