#!/usr/bin/env python3
"""
Comprehensive Speed Audit for All OpenAlgo Technical Indicators
Tests all 102 indicators with real market data across multiple dataset sizes
"""

import numpy as np
import pandas as pd
import time
import sys
import os
from datetime import datetime

# Add the parent directory to Python path to import openalgo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import ta

class SpeedAuditor:
    def __init__(self):
        self.results = {}
        self.errors = []
        
        # All 102 indicators from FUNCTION_ABBREVIATIONS_LIST.md
        self.indicators = {
            # Trend Indicators
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
            'frama': lambda data: ta.frama(data['high'], data['low'], data['close'], period=20),
            'trima': lambda data: ta.trima(data['close']),
            'vidya': lambda data: ta.vidya(data['close']),
            'mcginley': lambda data: ta.mcginley(data['close']),
            'supertrend': lambda data: ta.supertrend(data['high'], data['low'], data['close']),
            'ichimoku': lambda data: ta.ichimoku(data['high'], data['low'], data['close']),
            'alligator': lambda data: ta.alligator(data['close']),
            'ma_envelopes': lambda data: ta.ma_envelopes(data['close']),
            
            # Momentum Indicators
            'rsi': lambda data: ta.rsi(data['close']),
            'macd': lambda data: ta.macd(data['close']),
            'stochastic': lambda data: ta.stochastic(data['high'], data['low'], data['close']),
            'cci': lambda data: ta.cci(data['high'], data['low'], data['close']),
            'williams_r': lambda data: ta.williams_r(data['high'], data['low'], data['close']),
            'ultimate_oscillator': lambda data: ta.ultimate_oscillator(data['high'], data['low'], data['close']),
            'crsi': lambda data: ta.crsi(data['close']),
            'fisher': lambda data: ta.fisher(data['high'], data['low']),
            'elderray': lambda data: ta.elderray(data['high'], data['low'], data['close']),
            
            # Volatility Indicators
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
            'chaikin': lambda data: ta.chaikin(data['high'], data['low'], data['volume']),
            'rvol': lambda data: ta.rvol(data['volume']),
            'rvi': lambda data: ta.rvi(data['high'], data['low'], data['close']),
            'vi': lambda data: ta.vi(data['high'], data['low'], data['close']),
            'rwi': lambda data: ta.rwi(data['high'], data['low'], data['close']),
            
            # Volume Indicators
            'obv': lambda data: ta.obv(data['close'], data['volume']),
            'vwap': lambda data: ta.vwap(data['high'], data['low'], data['close'], data['volume']),
            'mfi': lambda data: ta.mfi(data['high'], data['low'], data['close'], data['volume']),
            'adl': lambda data: ta.adl(data['high'], data['low'], data['close'], data['volume']),
            'cmf': lambda data: ta.cmf(data['high'], data['low'], data['close'], data['volume']),
            'kvo': lambda data: ta.kvo(data['high'], data['low'], data['close'], data['volume']),
            'emv': lambda data: ta.emv(data['high'], data['low'], data['close'], data['volume']),
            'force_index': lambda data: ta.force_index(data['close'], data['volume']),
            'nvi': lambda data: ta.nvi(data['close'], data['volume']),
            'pvi': lambda data: ta.pvi(data['close'], data['volume']),
            'pvt': lambda data: ta.pvt(data['close'], data['volume']),
            'volosc': lambda data: ta.volosc(data['volume']),
            'vroc': lambda data: ta.vroc(data['volume']),
            
            # Oscillators Indicators
            'roc': lambda data: ta.roc(data['close']),
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
            'ht': lambda data: ta.ht(data['close']),
            'cho': lambda data: ta.cho(data['high'], data['low'], data['close']),
            'ckstop': lambda data: ta.ckstop(data['close']),
            'roc_oscillator': lambda data: ta.roc_oscillator(data['close']),
            'kst': lambda data: ta.kst(data['close']),
            'stc': lambda data: ta.stc(data['close']),
            
            # Statistical Indicators
            'linreg': lambda data: ta.linreg(data['close'], period=20),
            'lrslope': lambda data: ta.lrslope(data['close']),
            'correlation': lambda data: ta.correlation(data['close'], data['high'], period=20),
            'beta': lambda data: ta.beta(data['close'], data['high'], period=20),
            'variance': lambda data: ta.variance(data['close'], period=20),
            'stdev': lambda data: ta.stdev(data['close'], period=20),
            'stddev': lambda data: ta.stddev(data['close'], period=20),
            'tsf': lambda data: ta.tsf(data['close'], period=20),
            'median': lambda data: ta.median(data['close'], period=20),
            
            # Hybrid Indicators
            'adx': lambda data: ta.adx(data['high'], data['low'], data['close']),
            'dmi': lambda data: ta.dmi(data['high'], data['low'], data['close']),
            'parabolic_sar': lambda data: ta.parabolic_sar(data['high'], data['low']),
            'psar': lambda data: ta.psar(data['high'], data['low']),
            'pivot_points': lambda data: ta.pivot_points(data['high'], data['low'], data['close']),
            'fractals': lambda data: ta.fractals(data['high'], data['low']),
            'zigzag': lambda data: ta.zigzag(data['high'], data['low'], data['close']),
            'gator_oscillator': lambda data: ta.gator_oscillator(data['close']),
            'mode': lambda data: ta.mode(data['close']),
            
            # Utility Indicators
            'crossover': lambda data: ta.crossover(data['close'], data['open']),
            'crossunder': lambda data: ta.crossunder(data['close'], data['open']),
            'highest': lambda data: ta.highest(data['high'], period=20),
            'lowest': lambda data: ta.lowest(data['low'], period=20),
            'change': lambda data: ta.change(data['close']),
        }

    def generate_realistic_data(self, size: int) -> dict:
        """Generate realistic OHLCV data for testing"""
        np.random.seed(42)  # For reproducible results
        
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
            # Generate price with trend and noise
            trend = 0.0001 * np.sin(i / 100)  # Long-term sine wave trend
            noise = np.random.normal(0, 0.02)  # 2% daily volatility
            
            if i == 0:
                close = base_price
                open_price = base_price
            else:
                daily_return = trend + noise
                open_price = data['close'][-1]
                close = open_price * (1 + daily_return)
            
            # Generate realistic OHLC from close
            daily_range = abs(np.random.normal(0, 0.015)) * close
            high = close + daily_range * np.random.uniform(0.2, 0.8)
            low = close - daily_range * np.random.uniform(0.2, 0.8)
            
            # Ensure OHLC consistency
            high = max(high, close, open_price)
            low = min(low, close, open_price)
            
            # Generate volume with some correlation to price movement
            volume_base = base_volume * (0.5 + np.random.uniform(0, 1))
            price_change = abs((close - open_price) / open_price)
            volume_mult = 1 + price_change * 2  # Higher volume on bigger moves
            volume = int(volume_base * volume_mult)
            
            data['open'].append(open_price)
            data['high'].append(high)
            data['low'].append(low)
            data['close'].append(close)
            data['volume'].append(volume)
        
        return {k: np.array(v) for k, v in data.items()}

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
            
            # Handle tuple results (like MACD, Stochastic, etc.)
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

    def run_audit(self, dataset_sizes: list = [1000, 10000, 100000]):
        """Run complete speed audit"""
        print("OpenAlgo Technical Indicators - Comprehensive Speed Audit")
        print("=" * 80)
        print(f"Testing {len(self.indicators)} indicators across {len(dataset_sizes)} dataset sizes")
        print()
        
        for size in dataset_sizes:
            print(f"Generating {size:,} data points...")
            data = self.generate_realistic_data(size)
            
            print(f"Testing {len(self.indicators)} indicators with {size:,} data points...")
            size_results = {}
            size_errors = []
            
            total_time = 0
            successful_tests = 0
            
            for i, (name, func) in enumerate(self.indicators.items(), 1):
                print(f"  [{i:3d}/{len(self.indicators)}] Testing {name}...", end=" ", flush=True)
                
                exec_time, success, message = self.benchmark_indicator(name, func, data)
                total_time += exec_time
                
                if success:
                    successful_tests += 1
                    size_results[name] = exec_time
                    print(f"{exec_time:.3f}ms OK")
                else:
                    size_errors.append((name, message))
                    size_results[name] = None
                    print(f"ERROR: {message}")
            
            self.results[size] = size_results
            self.errors.extend([(size, name, error) for name, error in size_errors])
            
            print(f"\nDataset {size:,} Summary:")
            print(f"  Success Rate: {successful_tests}/{len(self.indicators)} ({successful_tests/len(self.indicators)*100:.1f}%)")
            print(f"  Total Time: {total_time/1000:.3f}s")
            print(f"  Average Time: {total_time/len(self.indicators):.2f}ms per indicator")
            print()

    def generate_report(self) -> str:
        """Generate comprehensive markdown report"""
        report_lines = []
        report_lines.append("# OpenAlgo Technical Indicators - Comprehensive Speed Audit Report")
        report_lines.append("")
        report_lines.append("## Executive Summary")
        report_lines.append("")
        
        dataset_sizes = sorted(self.results.keys())
        
        # Summary table
        report_lines.append("| Dataset Size | Success Rate | Total Time | Avg Time/Indicator | Fastest | Slowest |")
        report_lines.append("|-------------|--------------|------------|-------------------|---------|---------|")
        
        for size in dataset_sizes:
            results = self.results[size]
            valid_times = [t for t in results.values() if t is not None]
            total_time = sum(valid_times)
            success_rate = len(valid_times) / len(results) * 100
            avg_time = total_time / len(results) if results else 0
            fastest = min(valid_times) if valid_times else 0
            slowest = max(valid_times) if valid_times else 0
            
            report_lines.append(f"| {size:,} points | {success_rate:.1f}% | {total_time/1000:.3f}s | {avg_time:.2f}ms | {fastest:.3f}ms | {slowest:.1f}ms |")
        
        report_lines.append("")
        report_lines.append("## Detailed Performance Results")
        report_lines.append("")
        
        # Group indicators by category
        categories = {
            'Trend Indicators': ['sma', 'ema', 'wma', 'dema', 'tema', 'hma', 'vwma', 'alma', 'kama', 'zlema', 't3', 'frama', 'trima', 'vidya', 'mcginley', 'supertrend', 'ichimoku', 'alligator', 'ma_envelopes'],
            'Momentum Indicators': ['rsi', 'macd', 'stochastic', 'cci', 'williams_r', 'ultimate_oscillator', 'crsi', 'fisher', 'elderray'],
            'Volatility Indicators': ['bbands', 'atr', 'natr', 'true_range', 'keltner', 'donchian', 'bbpercent', 'bbwidth', 'starc', 'ulcerindex', 'hv', 'chandelier_exit', 'massindex', 'chaikin', 'rvol', 'rvi', 'vi', 'rwi'],
            'Volume Indicators': ['obv', 'vwap', 'mfi', 'adl', 'cmf', 'kvo', 'emv', 'force_index', 'nvi', 'pvi', 'pvt', 'volosc', 'vroc'],
            'Oscillators Indicators': ['roc', 'cmo', 'trix', 'ppo', 'po', 'dpo', 'awesome_oscillator', 'accelerator_oscillator', 'stochrsi', 'tsi', 'chop', 'aroon', 'aroon_oscillator', 'bop', 'ht', 'cho', 'ckstop', 'roc_oscillator', 'kst', 'stc'],
            'Statistical Indicators': ['linreg', 'lrslope', 'correlation', 'beta', 'variance', 'stdev', 'stddev', 'tsf', 'median'],
            'Hybrid Indicators': ['adx', 'dmi', 'parabolic_sar', 'psar', 'pivot_points', 'fractals', 'zigzag', 'gator_oscillator', 'mode'],
            'Utility Indicators': ['crossover', 'crossunder', 'highest', 'lowest', 'change']
        }
        
        for category, indicators in categories.items():
            report_lines.append(f"### {category}")
            report_lines.append("")
            report_lines.append("| Indicator | 1K (ms) | 10K (ms) | 100K (ms) | Scaling Ratio | Status |")
            report_lines.append("|-----------|---------|----------|-----------|---------------|---------|")
            
            for indicator in indicators:
                if indicator in self.indicators:
                    row_data = []
                    times = []
                    
                    for size in [1000, 10000, 100000]:
                        if size in self.results and indicator in self.results[size]:
                            time_ms = self.results[size][indicator]
                            if time_ms is not None:
                                times.append(time_ms)
                                row_data.append(f"{time_ms:.3f}")
                            else:
                                row_data.append("❌")
                        else:
                            row_data.append("-")
                    
                    # Calculate scaling ratio
                    if len(times) >= 2:
                        scaling_ratio = times[-1] / times[0] if times[0] > 0 else 0
                        scaling_str = f"{scaling_ratio:.1f}x"
                    else:
                        scaling_str = "-"
                    
                    # Status
                    status = "OK" if len(times) == 3 else "ERROR"
                    
                    report_lines.append(f"| {indicator} | {' | '.join(row_data)} | {scaling_str} | {status} |")
            
            report_lines.append("")
        
        # Performance Analysis
        report_lines.append("## Performance Analysis")
        report_lines.append("")
        
        if self.errors:
            report_lines.append("### Errors Encountered")
            report_lines.append("")
            for size, name, error in self.errors:
                report_lines.append(f"- **{name}** ({size:,} points): {error}")
            report_lines.append("")
        
        # Best and worst performers
        if 100000 in self.results:
            large_results = {k: v for k, v in self.results[100000].items() if v is not None}
            if large_results:
                fastest_indicators = sorted(large_results.items(), key=lambda x: x[1])[:10]
                slowest_indicators = sorted(large_results.items(), key=lambda x: x[1], reverse=True)[:10]
                
                report_lines.append("### Fastest Indicators (100K dataset)")
                report_lines.append("")
                for name, time_ms in fastest_indicators:
                    report_lines.append(f"- **{name}**: {time_ms:.3f}ms")
                report_lines.append("")
                
                report_lines.append("### Slowest Indicators (100K dataset)")
                report_lines.append("")
                for name, time_ms in slowest_indicators:
                    report_lines.append(f"- **{name}**: {time_ms:.3f}ms")
                report_lines.append("")
        
        # Footer
        report_lines.append("---")
        report_lines.append(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report_lines.append("*OpenAlgo Comprehensive Speed Audit*")
        
        return "\n".join(report_lines)

def main():
    """Main execution function"""
    auditor = SpeedAuditor()
    
    # Run the audit
    auditor.run_audit([1000, 10000, 100000])
    
    # Generate and save report
    report = auditor.generate_report()
    
    # Write report to file
    report_path = "comprehensive_speed_audit_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nComprehensive speed audit completed!")
    print(f"Report saved to: {report_path}")
    print(f"Tested {len(auditor.indicators)} indicators")
    
    if auditor.errors:
        print(f"Warning: {len(auditor.errors)} errors encountered")
        print("Check the report for details.")

if __name__ == "__main__":
    main()