#!/usr/bin/env python3
"""
Comprehensive Speed Audit with Real Market Data Patterns
Tests all OpenAlgo indicators with realistic market scenarios
"""

import numpy as np
import pandas as pd
import time
import sys
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

class MarketDataGenerator:
    """Generate realistic market data with various patterns"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
    
    def generate_trending_market(self, size: int, trend: float = 0.0005) -> dict:
        """Generate trending market data"""
        base_price = 100.0
        base_volume = 1000000
        
        data = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
        
        for i in range(size):
            if i == 0:
                close = base_price
                open_price = base_price
            else:
                # Trend with noise
                daily_return = trend + np.random.normal(0, 0.02)
                open_price = data['close'][-1]
                close = open_price * (1 + daily_return)
            
            # Generate realistic OHLC
            daily_range = abs(np.random.normal(0, 0.015)) * close
            high = close + daily_range * np.random.uniform(0.3, 0.7)
            low = close - daily_range * np.random.uniform(0.3, 0.7)
            
            # Ensure OHLC consistency
            high = max(high, close, open_price)
            low = min(low, close, open_price)
            
            # Volume correlates with volatility
            volatility = abs((close - open_price) / open_price)
            volume = int(base_volume * (0.5 + np.random.uniform(0, 1)) * (1 + volatility * 3))
            
            data['open'].append(open_price)
            data['high'].append(high)
            data['low'].append(low)
            data['close'].append(close)
            data['volume'].append(volume)
        
        return {k: np.array(v) for k, v in data.items()}
    
    def generate_volatile_market(self, size: int) -> dict:
        """Generate highly volatile market data"""
        base_price = 100.0
        base_volume = 1000000
        
        data = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
        
        for i in range(size):
            if i == 0:
                close = base_price
                open_price = base_price
            else:
                # High volatility with occasional large moves
                volatility = 0.03 if np.random.random() > 0.95 else 0.015
                daily_return = np.random.normal(0, volatility)
                open_price = data['close'][-1]
                close = open_price * (1 + daily_return)
            
            # Generate wider ranges
            daily_range = abs(np.random.normal(0, 0.025)) * close
            high = close + daily_range * np.random.uniform(0.4, 0.8)
            low = close - daily_range * np.random.uniform(0.4, 0.8)
            
            high = max(high, close, open_price)
            low = min(low, close, open_price)
            
            # Higher volume on volatile days
            price_change = abs((close - open_price) / open_price)
            volume = int(base_volume * (1 + price_change * 5) * np.random.uniform(0.5, 2))
            
            data['open'].append(open_price)
            data['high'].append(high)
            data['low'].append(low)
            data['close'].append(close)
            data['volume'].append(volume)
        
        return {k: np.array(v) for k, v in data.items()}

class ComprehensiveAuditor:
    def __init__(self):
        self.results = {}
        self.errors = []
        
        # All 102 indicators with proper parameters
        self.indicators = {
            # Trend Indicators (19)
            'sma': lambda data: ta.sma(data['close'], period=20),
            'ema': lambda data: ta.ema(data['close'], period=20),
            'wma': lambda data: ta.wma(data['close'], period=20),
            'dema': lambda data: ta.dema(data['close'], period=20),
            'tema': lambda data: ta.tema(data['close'], period=20),
            'hma': lambda data: ta.hma(data['close'], period=20),
            'vwma': lambda data: ta.vwma(data['close'], data['volume'], period=20),
            'alma': lambda data: ta.alma(data['close']),
            'kama': lambda data: ta.kama(data['close']),
            'zlema': lambda data: ta.zlema(data['close'], period=20),
            't3': lambda data: ta.t3(data['close']),
            'frama': lambda data: ta.frama(data['high'], data['low'], period=20),
            'trima': lambda data: ta.trima(data['close']),
            'vidya': lambda data: ta.vidya(data['close']),
            'mcginley': lambda data: ta.mcginley(data['close']),
            'supertrend': lambda data: ta.supertrend(data['high'], data['low'], data['close']),
            'ichimoku': lambda data: ta.ichimoku(data['high'], data['low'], data['close']),
            'alligator': lambda data: ta.alligator(data['close']),
            'ma_envelopes': lambda data: ta.ma_envelopes(data['close']),
            
            # Momentum Indicators (9)
            'rsi': lambda data: ta.rsi(data['close']),
            'macd': lambda data: ta.macd(data['close']),
            'stochastic': lambda data: ta.stochastic(data['high'], data['low'], data['close']),
            'cci': lambda data: ta.cci(data['high'], data['low'], data['close']),
            'williams_r': lambda data: ta.williams_r(data['high'], data['low'], data['close']),
            'ultimate_oscillator': lambda data: ta.ultimate_oscillator(data['high'], data['low'], data['close']),
            'crsi': lambda data: ta.crsi(data['close']),
            'fisher': lambda data: ta.fisher(data['high'], data['low']),
            'elderray': lambda data: ta.elderray(data['high'], data['low'], data['close']),
            
            # Volatility Indicators (18)
            'bbands': lambda data: ta.bbands(data['close']),
            'atr': lambda data: ta.atr(data['high'], data['low'], data['close']),
            'natr': lambda data: ta.natr(data['high'], data['low'], data['close']),
            'true_range': lambda data: ta.true_range(data['high'], data['low'], data['close']),
            'keltner': lambda data: ta.keltner(data['high'], data['low'], data['close']),
            'donchian': lambda data: ta.donchian(data['high'], data['low']),
            'bbpercent': lambda data: ta.bbpercent(data['close']),
            'bbwidth': lambda data: ta.bbwidth(data['close']),
            'starc': lambda data: ta.starc(data['high'], data['low'], data['close']),
            'ulcerindex': lambda data: ta.ulcerindex(data['close']),
            'hv': lambda data: ta.hv(data['close']),
            'chandelier_exit': lambda data: ta.chandelier_exit(data['high'], data['low'], data['close']),
            'massindex': lambda data: ta.massindex(data['high'], data['low']),
            'chaikin': lambda data: ta.chaikin(data['high'], data['low']),
            'rvol': lambda data: ta.rvol(data['volume']),
            'rvi': lambda data: ta.rvi(data['open'], data['high'], data['low'], data['close']),
            'vi': lambda data: ta.vi(data['high'], data['low'], data['close']),
            'rwi': lambda data: ta.rwi(data['high'], data['low'], data['close']),
            
            # Volume Indicators (13)
            'obv': lambda data: ta.obv(data['close'], data['volume']),
            'vwap': lambda data: ta.vwap(data['high'], data['low'], data['close'], data['volume']),
            'mfi': lambda data: ta.mfi(data['high'], data['low'], data['close'], data['volume']),
            'adl': lambda data: ta.adl(data['high'], data['low'], data['close'], data['volume']),
            'cmf': lambda data: ta.cmf(data['high'], data['low'], data['close'], data['volume']),
            'kvo': lambda data: ta.kvo(data['high'], data['low'], data['close'], data['volume']),
            'emv': lambda data: ta.emv(data['high'], data['low'], data['volume']),
            'force_index': lambda data: ta.force_index(data['close'], data['volume']),
            'nvi': lambda data: ta.nvi(data['close'], data['volume']),
            'pvi': lambda data: ta.pvi(data['close'], data['volume']),
            'pvt': lambda data: ta.pvt(data['close'], data['volume']),
            'volosc': lambda data: ta.volosc(data['volume']),
            'vroc': lambda data: ta.vroc(data['volume']),
            
            # Oscillators Indicators (20)
            'roc': lambda data: ta.roc(data['close'], length=12),
            'cmo': lambda data: ta.cmo(data['close']),
            'trix': lambda data: ta.trix(data['close']),
            'ppo': lambda data: ta.ppo(data['close']),
            'po': lambda data: ta.po(data['close']),
            'dpo': lambda data: ta.dpo(data['close']),
            'awesome_oscillator': lambda data: ta.awesome_oscillator(data['high'], data['low']),
            'accelerator_oscillator': lambda data: ta.accelerator_oscillator(data['high'], data['low']),
            'stochrsi': lambda data: ta.stochrsi(data['close']),
            'tsi': lambda data: ta.tsi(data['close']),
            'chop': lambda data: ta.chop(data['high'], data['low'], data['close']),
            'aroon': lambda data: ta.aroon(data['high'], data['low']),
            'aroon_oscillator': lambda data: ta.aroon_oscillator(data['high'], data['low']),
            'bop': lambda data: ta.bop(data['open'], data['high'], data['low'], data['close']),
            'ht': lambda data: ta.ht(data['close'], data['high'], data['low']),
            'cho': lambda data: ta.cho(data['high'], data['low'], data['close'], data['volume']),
            'ckstop': lambda data: ta.ckstop(data['high'], data['low'], data['close']),
            'roc_oscillator': lambda data: ta.roc_oscillator(data['close']),
            'kst': lambda data: ta.kst(data['close']),
            'stc': lambda data: ta.stc(data['close']),
            
            # Statistical Indicators (9)
            'linreg': lambda data: ta.linreg(data['close'], period=20),
            'lrslope': lambda data: ta.lrslope(data['close']),
            'correlation': lambda data: ta.correlation(data['close'], data['high'], period=20),
            'beta': lambda data: ta.beta(data['close'], data['high'], period=20),
            'variance': lambda data: ta.variance(data['close'], period=20),
            'stdev': lambda data: ta.stdev(data['close'], period=20),
            'stddev': lambda data: ta.stddev(data['close'], period=20),
            'tsf': lambda data: ta.tsf(data['close'], period=20),
            'median': lambda data: ta.median(data['close'], period=20),
            
            # Hybrid Indicators (9)
            'adx': lambda data: ta.adx(data['high'], data['low'], data['close']),
            'dmi': lambda data: ta.dmi(data['high'], data['low'], data['close']),
            'parabolic_sar': lambda data: ta.parabolic_sar(data['high'], data['low']),
            'psar': lambda data: ta.psar(data['high'], data['low']),
            'pivot_points': lambda data: ta.pivot_points(data['high'], data['low'], data['close']),
            'fractals': lambda data: ta.fractals(data['high'], data['low']),
            'zigzag': lambda data: ta.zigzag(data['high'], data['low'], data['close']),
            'gator_oscillator': lambda data: ta.gator_oscillator(data['high'], data['low']),
            'mode': lambda data: ta.mode(data['close']),
            
            # Utility Indicators (5) 
            'crossover': lambda data: ta.crossover(data['close'], data['open']),
            'crossunder': lambda data: ta.crossunder(data['close'], data['open']),
            'highest': lambda data: ta.highest(data['high'], period=20),
            'lowest': lambda data: ta.lowest(data['low'], period=20),
            'change': lambda data: ta.change(data['close']),
        }
        
        print(f"Loaded {len(self.indicators)} indicators for testing")

    def benchmark_indicator(self, name: str, func, data: dict) -> tuple:
        """Benchmark a single indicator"""
        try:
            start_time = time.perf_counter()
            result = func(data)
            end_time = time.perf_counter()
            
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
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

    def run_comprehensive_audit(self):
        """Run the comprehensive audit"""
        generator = MarketDataGenerator()
        
        print("OpenAlgo Technical Indicators - Comprehensive Speed Audit")
        print("=" * 80)
        print(f"Testing {len(self.indicators)} indicators with realistic market data")
        print()
        
        # Test scenarios
        scenarios = [
            ("Trending Market (1K)", lambda: generator.generate_trending_market(1000, trend=0.001)),
            ("Volatile Market (1K)", lambda: generator.generate_volatile_market(1000)),
            ("Large Dataset (10K)", lambda: generator.generate_trending_market(10000, trend=0.0002)),
            ("Extra Large (100K)", lambda: generator.generate_trending_market(100000, trend=0.0001)),
        ]
        
        for scenario_name, data_generator in scenarios:
            print(f"Testing: {scenario_name}")
            print("-" * 60)
            
            data = data_generator()
            print(f"Generated {len(data['close']):,} data points")
            print(f"Price range: ${data['close'].min():.2f} - ${data['close'].max():.2f}")
            print(f"Volume range: {data['volume'].min():,} - {data['volume'].max():,}")
            print()
            
            scenario_results = {}
            successful_tests = 0
            total_time = 0
            
            for i, (name, func) in enumerate(self.indicators.items(), 1):
                print(f"  [{i:3d}/{len(self.indicators)}] {name:<20}", end=" ", flush=True)
                
                exec_time, success, message = self.benchmark_indicator(name, func, data)
                total_time += exec_time
                
                if success:
                    successful_tests += 1
                    scenario_results[name] = exec_time
                    print(f"{exec_time:8.3f}ms OK")
                else:
                    scenario_results[name] = None
                    self.errors.append((scenario_name, name, message))
                    print(f"        ERROR: {message}")
            
            self.results[scenario_name] = scenario_results
            
            print(f"\n{scenario_name} Summary:")
            print(f"  Success Rate: {successful_tests}/{len(self.indicators)} ({successful_tests/len(self.indicators)*100:.1f}%)")
            print(f"  Total Time: {total_time/1000:.3f}s")
            print(f"  Average Time: {total_time/len(self.indicators):.2f}ms per indicator")
            
            if successful_tests > 0:
                valid_times = [t for t in scenario_results.values() if t is not None]
                print(f"  Fastest: {min(valid_times):.3f}ms")
                print(f"  Slowest: {max(valid_times):.3f}ms")
            
            print()

    def generate_summary_report(self) -> str:
        """Generate a summary report"""
        report_lines = []
        report_lines.append("# OpenAlgo Technical Indicators - Comprehensive Real Data Audit")
        report_lines.append("")
        report_lines.append("## Executive Summary")
        report_lines.append("")
        
        scenarios = list(self.results.keys())
        
        # Summary table
        report_lines.append("| Scenario | Success Rate | Total Time | Avg Time | Fastest | Slowest |")
        report_lines.append("|----------|--------------|------------|----------|---------|---------|")
        
        for scenario in scenarios:
            results = self.results[scenario]
            valid_times = [t for t in results.values() if t is not None]
            if valid_times:
                total_time = sum(valid_times)
                success_rate = len(valid_times) / len(results) * 100
                avg_time = total_time / len(results)
                fastest = min(valid_times)
                slowest = max(valid_times)
                
                report_lines.append(f"| {scenario} | {success_rate:.1f}% | {total_time/1000:.3f}s | {avg_time:.2f}ms | {fastest:.3f}ms | {slowest:.1f}ms |")
        
        report_lines.append("")
        
        # Error summary
        if self.errors:
            report_lines.append("## Errors Encountered")
            report_lines.append("")
            for scenario, name, error in self.errors:
                report_lines.append(f"- **{name}** in {scenario}: {error}")
            report_lines.append("")
        
        # Performance ranking (using Large Dataset)
        if "Large Dataset (10K)" in self.results:
            large_results = {k: v for k, v in self.results["Large Dataset (10K)"].items() if v is not None}
            if large_results:
                sorted_results = sorted(large_results.items(), key=lambda x: x[1])
                
                report_lines.append("## Performance Ranking (10K Dataset)")
                report_lines.append("")
                report_lines.append("### Top 10 Fastest Indicators")
                report_lines.append("")
                for i, (name, time_ms) in enumerate(sorted_results[:10], 1):
                    report_lines.append(f"{i:2d}. **{name}**: {time_ms:.3f}ms")
                
                report_lines.append("")
                report_lines.append("### Top 10 Slowest Indicators")
                report_lines.append("")
                for i, (name, time_ms) in enumerate(sorted_results[-10:][::-1], 1):
                    report_lines.append(f"{i:2d}. **{name}**: {time_ms:.3f}ms")
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report_lines.append(f"*Tested {len(self.indicators)} indicators*")
        
        return "\n".join(report_lines)

def main():
    """Main execution"""
    auditor = ComprehensiveAuditor()
    
    # Run the audit
    auditor.run_comprehensive_audit()
    
    # Generate and save report
    report = auditor.generate_summary_report()
    
    report_path = "comprehensive_real_data_audit_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("=" * 80)
    print("COMPREHENSIVE AUDIT COMPLETED")
    print("=" * 80)
    print(f"Report saved to: {report_path}")
    print(f"Total indicators tested: {len(auditor.indicators)}")
    print(f"Total scenarios: {len(auditor.results)}")
    
    if auditor.errors:
        print(f"Errors encountered: {len(auditor.errors)}")
    else:
        print("All indicators working correctly!")

if __name__ == "__main__":
    main()