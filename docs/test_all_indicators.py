#!/usr/bin/env python3
"""
Comprehensive test script for all 102 technical indicators in OpenAlgo library
Tests each indicator with sample data to validate functionality
"""

import numpy as np
import pandas as pd
import sys
import traceback
from typing import Union, Tuple, Any

# Add the openalgo package to path
sys.path.insert(0, '/Users/openalgo/openalgo-python-library/openalgo-python-library')

try:
    from openalgo import ta
    print("✓ Successfully imported OpenAlgo library")
except ImportError as e:
    print(f"✗ Failed to import OpenAlgo library: {e}")
    sys.exit(1)

class IndicatorTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
        # Generate sample data for testing
        np.random.seed(42)  # For reproducible results
        self.length = 100
        
        # Price data
        base_price = 100
        price_changes = np.random.randn(self.length) * 0.02
        self.close = base_price * np.exp(np.cumsum(price_changes))
        
        # OHLCV data
        self.open = self.close * (1 + np.random.randn(self.length) * 0.001)
        self.high = np.maximum(self.open, self.close) * (1 + np.abs(np.random.randn(self.length)) * 0.01)
        self.low = np.minimum(self.open, self.close) * (1 - np.abs(np.random.randn(self.length)) * 0.01)
        self.volume = np.random.randint(1000, 10000, self.length).astype(float)
        
        print(f"Generated test data: {self.length} periods")
        print(f"Price range: ${self.close.min():.2f} - ${self.close.max():.2f}")
    
    def test_indicator(self, name: str, func_call: callable, expected_type: type = None) -> bool:
        """Test a single indicator function"""
        try:
            result = func_call()
            
            # Basic validation
            if result is None:
                raise ValueError("Function returned None")
            
            # Type checking
            if isinstance(result, tuple):
                # Multi-output indicator
                for i, component in enumerate(result):
                    if not isinstance(component, (np.ndarray, pd.Series)):
                        raise ValueError(f"Component {i} has invalid type: {type(component)}")
                    if len(component) == 0:
                        raise ValueError(f"Component {i} is empty")
            else:
                # Single output indicator
                if not isinstance(result, (np.ndarray, pd.Series)):
                    raise ValueError(f"Invalid return type: {type(result)}")
                if len(result) == 0:
                    raise ValueError("Result is empty")
            
            print(f"✓ {name}")
            self.passed += 1
            return True
            
        except Exception as e:
            error_msg = f"✗ {name}: {str(e)}"
            print(error_msg)
            self.errors.append(f"{name}: {str(e)}")
            self.failed += 1
            return False
    
    def run_all_tests(self):
        """Test all 102 indicators from the abbreviations list"""
        print("\n" + "="*60)
        print("TESTING ALL 102 TECHNICAL INDICATORS")
        print("="*60)
        
        # 1. TREND INDICATORS
        print("\n--- TREND INDICATORS ---")
        self.test_indicator("sma", lambda: ta.sma(self.close, 20))
        self.test_indicator("ema", lambda: ta.ema(self.close, 20))
        self.test_indicator("wma", lambda: ta.wma(self.close, 20))
        self.test_indicator("dema", lambda: ta.dema(self.close, 20))
        self.test_indicator("tema", lambda: ta.tema(self.close, 20))
        self.test_indicator("hma", lambda: ta.hma(self.close, 20))
        self.test_indicator("vwma", lambda: ta.vwma(self.close, self.volume, 20))
        self.test_indicator("alma", lambda: ta.alma(self.close, 21, 0.85, 6.0))
        self.test_indicator("kama", lambda: ta.kama(self.close, 10, 2, 30))
        self.test_indicator("zlema", lambda: ta.zlema(self.close, 20))
        self.test_indicator("t3", lambda: ta.t3(self.close, 21, 0.7))
        self.test_indicator("frama", lambda: ta.frama(self.close, 16))
        self.test_indicator("trima", lambda: ta.trima(self.close, 20))
        self.test_indicator("supertrend", lambda: ta.supertrend(self.high, self.low, self.close, 10, 3.0))
        self.test_indicator("ichimoku", lambda: ta.ichimoku(self.high, self.low, self.close, 9, 26, 52, 26))
        self.test_indicator("alligator", lambda: ta.alligator(self.high, self.low, 13, 8, 8, 5, 5, 3))
        self.test_indicator("ma_envelopes", lambda: ta.ma_envelopes(self.close, 20, 2.5, 'SMA'))
        self.test_indicator("mcginley", lambda: ta.mcginley(self.close, 14))
        self.test_indicator("vidya", lambda: ta.vidya(self.close, 14, 0.2))
        
        # 2. MOMENTUM INDICATORS
        print("\n--- MOMENTUM INDICATORS ---")
        self.test_indicator("rsi", lambda: ta.rsi(self.close, 14))
        self.test_indicator("macd", lambda: ta.macd(self.close, 12, 26, 9))
        self.test_indicator("stochastic", lambda: ta.stochastic(self.high, self.low, self.close, 14, 3))
        self.test_indicator("cci", lambda: ta.cci(self.high, self.low, self.close, 20))
        self.test_indicator("williams_r", lambda: ta.williams_r(self.high, self.low, self.close, 14))
        self.test_indicator("bop", lambda: ta.bop(self.open, self.high, self.low, self.close))
        self.test_indicator("elderray", lambda: ta.elderray(self.high, self.low, self.close, 13))
        self.test_indicator("fisher", lambda: ta.fisher((self.high + self.low) / 2, 10))
        self.test_indicator("crsi", lambda: ta.crsi(self.close, 3, 2, 100))
        
        # 3. VOLATILITY INDICATORS
        print("\n--- VOLATILITY INDICATORS ---")
        self.test_indicator("atr", lambda: ta.atr(self.high, self.low, self.close, 14))
        self.test_indicator("bbands", lambda: ta.bbands(self.close, 20, 2.0))
        self.test_indicator("bbpercent", lambda: ta.bbpercent(self.close, 20, 2.0))
        self.test_indicator("bbwidth", lambda: ta.bbwidth(self.close, 20, 2.0))
        self.test_indicator("keltner", lambda: ta.keltner(self.high, self.low, self.close, 20, 10, 2.0))
        self.test_indicator("donchian", lambda: ta.donchian(self.high, self.low, 20))
        self.test_indicator("chaikin", lambda: ta.chaikin(self.high, self.low, 10, 10))
        self.test_indicator("natr", lambda: ta.natr(self.high, self.low, self.close, 14))
        self.test_indicator("rvol", lambda: ta.rvol(self.close, 10, 14))
        self.test_indicator("ultimate_oscillator", lambda: ta.ultimate_oscillator(self.high, self.low, self.close, 7, 14, 28))
        self.test_indicator("stddev", lambda: ta.stddev(self.close, 20))
        self.test_indicator("stdev", lambda: ta.stdev(self.close, 20))
        self.test_indicator("true_range", lambda: ta.true_range(self.high, self.low, self.close))
        self.test_indicator("massindex", lambda: ta.massindex(self.high, self.low, 9, 25))
        self.test_indicator("chandelier_exit", lambda: ta.chandelier_exit(self.high, self.low, self.close, 22, 3.0))
        self.test_indicator("hv", lambda: ta.hv(self.close, 20, True))
        self.test_indicator("ulcerindex", lambda: ta.ulcerindex(self.close, 14))
        self.test_indicator("starc", lambda: ta.starc(self.high, self.low, self.close, 20, 15, 2.0))
        
        # 4. VOLUME INDICATORS
        print("\n--- VOLUME INDICATORS ---")
        self.test_indicator("obv", lambda: ta.obv(self.close, self.volume))
        self.test_indicator("vwap", lambda: ta.vwap(self.high, self.low, self.close, self.volume, 0))
        self.test_indicator("mfi", lambda: ta.mfi(self.high, self.low, self.close, self.volume, 14))
        self.test_indicator("adl", lambda: ta.adl(self.high, self.low, self.close, self.volume))
        self.test_indicator("cmf", lambda: ta.cmf(self.high, self.low, self.close, self.volume, 20))
        self.test_indicator("emv", lambda: ta.emv(self.high, self.low, self.volume, 1000000))
        self.test_indicator("force_index", lambda: ta.force_index(self.close, self.volume))
        self.test_indicator("nvi", lambda: ta.nvi(self.close, self.volume))
        self.test_indicator("pvi", lambda: ta.pvi(self.close, self.volume))
        self.test_indicator("volosc", lambda: ta.volosc(self.volume, 5, 10))
        self.test_indicator("vroc", lambda: ta.vroc(self.volume, 25))
        self.test_indicator("kvo", lambda: ta.kvo(self.high, self.low, self.close, self.volume, 34, 55))
        self.test_indicator("pvt", lambda: ta.pvt(self.close, self.volume))
        
        # 5. OSCILLATORS
        print("\n--- OSCILLATORS ---")
        self.test_indicator("roc", lambda: ta.roc(self.close, 12))
        self.test_indicator("roc_oscillator", lambda: ta.roc_oscillator(self.close, 12))
        self.test_indicator("cmo", lambda: ta.cmo(self.close, 14))
        self.test_indicator("trix", lambda: ta.trix(self.close, 14))
        self.test_indicator("uo_oscillator", lambda: ta.uo_oscillator(self.high, self.low, self.close, 7, 14, 28))
        self.test_indicator("awesome_oscillator", lambda: ta.awesome_oscillator(self.high, self.low, 5, 34))
        self.test_indicator("accelerator_oscillator", lambda: ta.accelerator_oscillator(self.high, self.low, 5))
        self.test_indicator("ppo", lambda: ta.ppo(self.close, 12, 26, 9))
        self.test_indicator("po", lambda: ta.po(self.close, 10, 20, "SMA"))
        self.test_indicator("dpo", lambda: ta.dpo(self.close, 20))
        self.test_indicator("aroon_oscillator", lambda: ta.aroon_oscillator(self.high, self.low, 25))
        self.test_indicator("stochrsi", lambda: ta.stochrsi(self.close, 14, 14, 3, 3))
        self.test_indicator("rvi", lambda: ta.rvi(self.open, self.high, self.low, self.close, 10))
        self.test_indicator("cho", lambda: ta.cho(self.high, self.low, self.close, self.volume, 3, 10))
        self.test_indicator("chop", lambda: ta.chop(self.high, self.low, self.close, 14))
        self.test_indicator("kst", lambda: ta.kst(self.close, 10, 15, 20, 30, 10, 10, 10, 15, 9))
        self.test_indicator("tsi", lambda: ta.tsi(self.close, 25, 13, 13))
        self.test_indicator("vi", lambda: ta.vi(self.high, self.low, self.close, 14))
        self.test_indicator("stc", lambda: ta.stc(self.close, 23, 50, 10, 3, 3))
        self.test_indicator("gator_oscillator", lambda: ta.gator_oscillator(self.close, 13, 8, 8, 5, 5, 3))
        
        # 6. STATISTICAL INDICATORS
        print("\n--- STATISTICAL INDICATORS ---")
        self.test_indicator("linreg", lambda: ta.linreg(self.close, 14))
        self.test_indicator("lrslope", lambda: ta.lrslope(self.close, 14))
        self.test_indicator("correlation", lambda: ta.correlation(self.close, self.volume, 20))
        self.test_indicator("beta", lambda: ta.beta(self.close, self.close * 1.1, 252))  # Using modified close as market
        self.test_indicator("variance", lambda: ta.variance(self.close, 20))
        self.test_indicator("tsf", lambda: ta.tsf(self.close, 14))
        self.test_indicator("median", lambda: ta.median(self.close, 20))
        self.test_indicator("mode", lambda: ta.mode(self.close, 20, 10))
        
        # 7. HYBRID INDICATORS
        print("\n--- HYBRID INDICATORS ---")
        self.test_indicator("adx", lambda: ta.adx(self.high, self.low, self.close, 14))
        self.test_indicator("aroon", lambda: ta.aroon(self.high, self.low, 25))
        self.test_indicator("pivot_points", lambda: ta.pivot_points(self.high, self.low, self.close))
        self.test_indicator("parabolic_sar", lambda: ta.parabolic_sar(self.high, self.low, 0.02, 0.2))
        self.test_indicator("dmi", lambda: ta.dmi(self.high, self.low, self.close, 14))
        self.test_indicator("psar", lambda: ta.psar(self.high, self.low, 0.02, 0.2))
        self.test_indicator("ht", lambda: ta.ht(self.close))
        self.test_indicator("ckstop", lambda: ta.ckstop(self.high, self.low, self.close, 10, 1.0))
        self.test_indicator("rwi", lambda: ta.rwi(self.high, self.low, self.close, 14))
        self.test_indicator("fractals", lambda: ta.fractals(self.high, self.low, 2))
        self.test_indicator("zigzag", lambda: ta.zigzag(self.high, self.low, 5.0))
        
        # 8. UTILITY FUNCTIONS
        print("\n--- UTILITY FUNCTIONS ---")
        self.test_indicator("crossover", lambda: ta.crossover(self.close, ta.sma(self.close, 20)))
        self.test_indicator("crossunder", lambda: ta.crossunder(self.close, ta.sma(self.close, 20)))
        self.test_indicator("highest", lambda: ta.highest(self.close, 20))
        self.test_indicator("lowest", lambda: ta.lowest(self.close, 20))
        self.test_indicator("change", lambda: ta.change(self.close, 1))
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed} ✓")
        print(f"Failed: {self.failed} ✗")
        print(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.errors:
            print(f"\nFAILED TESTS ({len(self.errors)}):")
            print("-" * 30)
            for error in self.errors:
                print(f"  • {error}")
        else:
            print("\n🎉 ALL INDICATORS PASSED!")
        
        return self.failed == 0

if __name__ == "__main__":
    print("OpenAlgo Technical Indicators - Comprehensive Test Suite")
    print("=" * 60)
    
    tester = IndicatorTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)