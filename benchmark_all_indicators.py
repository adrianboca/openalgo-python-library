#!/usr/bin/env python3
"""
Comprehensive Speed Benchmark for All 103 Technical Indicators
Testing with 1,000, 10,000, and 100,000 data points
"""

import numpy as np
import time
import json
from openalgo import ta

def generate_test_data(size):
    """Generate consistent test data for benchmarking"""
    np.random.seed(42)
    
    # Generate realistic OHLCV data
    returns = np.random.normal(0.001, 0.02, size)
    close = 100 * np.exp(np.cumsum(returns))
    high = close * np.random.uniform(1.005, 1.03, size)
    low = close * np.random.uniform(0.97, 0.995, size)
    open_price = close * np.random.uniform(0.995, 1.005, size)
    volume = np.random.randint(10000, 1000000, size).astype(float)
    
    # Ensure proper OHLC relationships
    high = np.maximum(high, close)
    low = np.minimum(low, close)
    
    return {
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }

def benchmark_indicator(name, test_func, iterations=3):
    """Benchmark a single indicator with multiple iterations"""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        try:
            result = test_func()
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        except Exception as e:
            return None, str(e)[:100]
    
    return np.mean(times), None

def run_comprehensive_benchmark():
    """Run benchmark for all 103 indicators"""
    
    print("="*80)
    print("COMPREHENSIVE SPEED BENCHMARK - ALL 103 INDICATORS")
    print("="*80)
    
    # Test sizes
    sizes = [1000, 10000, 100000]
    all_results = {}
    
    for size in sizes:
        print(f"\n📊 Benchmarking with {size:,} data points...")
        data = generate_test_data(size)
        
        # Extract data arrays
        open_price = data['open']
        high = data['high']
        low = data['low']
        close = data['close']
        volume = data['volume']
        
        # Pre-calculate SMA for crossover tests
        sma20 = ta.sma(close, 20)
        
        # Define all 103 indicator tests with correct parameters
        indicator_tests = {
            # Trend Indicators (19)
            'sma': lambda: ta.sma(close, 20),
            'ema': lambda: ta.ema(close, 20),
            'wma': lambda: ta.wma(close, 20),
            'dema': lambda: ta.dema(close, 20),
            'tema': lambda: ta.tema(close, 20),
            'hma': lambda: ta.hma(close, 20),
            'vwma': lambda: ta.vwma(close, volume, 20),
            'alma': lambda: ta.alma(close, 20),
            'kama': lambda: ta.kama(close, 10),
            'zlema': lambda: ta.zlema(close, 20),
            't3': lambda: ta.t3(close, 20),
            'frama': lambda: ta.frama(close, 20),
            'trima': lambda: ta.trima(close, 20),
            'vidya': lambda: ta.vidya(close, 20),
            'mcginley': lambda: ta.mcginley(close, 20),
            'supertrend': lambda: ta.supertrend(high, low, close, 10, 3.0),
            'ichimoku': lambda: ta.ichimoku(high, low, close),
            'alligator': lambda: ta.alligator((high + low + close) / 3),
            'ma_envelopes': lambda: ta.ma_envelopes(close, 20, 2.5),
            
            # Momentum Indicators (9)
            'rsi': lambda: ta.rsi(close, 14),
            'macd': lambda: ta.macd(close, 12, 26, 9),
            'stochastic': lambda: ta.stochastic(high, low, close, 14, 3),
            'cci': lambda: ta.cci(high, low, close, 20),
            'williams_r': lambda: ta.williams_r(high, low, close, 14),
            'ultimate_oscillator': lambda: ta.ultimate_oscillator(high, low, close),
            'crsi': lambda: ta.crsi(close, 3, 2, 100),
            'fisher': lambda: ta.fisher(close, 10),
            'elderray': lambda: ta.elderray(high, low, close, 13),
            
            # Volatility Indicators (18)
            'bbands': lambda: ta.bbands(close, 20, 2),
            'atr': lambda: ta.atr(high, low, close, 14),
            'natr': lambda: ta.natr(high, low, close, 14),
            'true_range': lambda: ta.true_range(high, low, close),
            'keltner': lambda: ta.keltner(high, low, close, 20),
            'donchian': lambda: ta.donchian(high, low, 20),
            'bbpercent': lambda: ta.bbpercent(close, 20, 2),
            'bbwidth': lambda: ta.bbwidth(close, 20, 2),
            'starc': lambda: ta.starc(high, low, close, 20, 2.0),
            'ulcerindex': lambda: ta.ulcerindex(close, 14),
            'hv': lambda: ta.hv(close, 20),
            'chandelier_exit': lambda: ta.chandelier_exit(high, low, close, 22, 3.0),
            'massindex': lambda: ta.massindex(high, low, 9, 25),
            'chaikin': lambda: ta.chaikin(high, low, 10, 10),
            'rvol': lambda: ta.rvol(close, 10, 14),
            'rvi': lambda: ta.rvi(open_price, high, low, close, 10),
            'vi': lambda: ta.vi(high, low, close, 14),
            'rwi': lambda: ta.rwi(high, low, close, 14),
            
            # Volume Indicators (13)
            'obv': lambda: ta.obv(close, volume),
            'vwap': lambda: ta.vwap(high, low, close, volume),
            'mfi': lambda: ta.mfi(high, low, close, volume, 14),
            'adl': lambda: ta.adl(high, low, close, volume),
            'cmf': lambda: ta.cmf(high, low, close, volume, 20),
            'kvo': lambda: ta.kvo(high, low, close, volume),
            'emv': lambda: ta.emv(high, low, volume),
            'force_index': lambda: ta.force_index(close, volume),
            'nvi': lambda: ta.nvi(close, volume),
            'pvi': lambda: ta.pvi(close, volume),
            'pvt': lambda: ta.pvt(close, volume),
            'volosc': lambda: ta.volosc(volume, 5, 10),
            'vroc': lambda: ta.vroc(volume, 12),
            
            # Oscillators (20)
            'roc': lambda: ta.roc(close, 12),
            'cmo': lambda: ta.cmo(close, 14),
            'trix': lambda: ta.trix(close, 14),
            'ppo': lambda: ta.ppo(close, 12, 26),
            'po': lambda: ta.po(close, 20),
            'dpo': lambda: ta.dpo(close, 20),
            'awesome_oscillator': lambda: ta.awesome_oscillator(high, low),
            'accelerator_oscillator': lambda: ta.accelerator_oscillator(high, low, 5),
            'stochrsi': lambda: ta.stochrsi(close, 14, 14, 3, 3),
            'tsi': lambda: ta.tsi(close, 25, 13, 13),
            'chop': lambda: ta.chop(high, low, close, 14),
            'aroon': lambda: ta.aroon(high, low, 25),
            'aroon_oscillator': lambda: ta.aroon_oscillator(high, low, 25),
            'bop': lambda: ta.bop(open_price, high, low, close),
            'ht': lambda: ta.ht(close),
            'cho': lambda: ta.cho(high, low, close, volume),
            'ckstop': lambda: ta.ckstop(high, low, close, 10, 3.0),
            'roc_oscillator': lambda: ta.roc_oscillator(close, 12),
            'kst': lambda: ta.kst(close),
            'stc': lambda: ta.stc(close, 23, 50, 10, 3, 3),
            
            # Statistical Indicators (9)
            'linreg': lambda: ta.linreg(close, 14),
            'lrslope': lambda: ta.lrslope(close, 14),
            'correlation': lambda: ta.correlation(close, volume, 20),
            'beta': lambda: ta.beta(close, close, 252),
            'variance': lambda: ta.variance(close, 20),
            'stdev': lambda: ta.stdev(close, 20),
            'stddev': lambda: ta.stddev(close, 20),
            'tsf': lambda: ta.tsf(close, 14),
            'median': lambda: ta.median(close, 20),
            
            # Hybrid Indicators (11)
            'adx': lambda: ta.adx(high, low, close, 14),
            'dmi': lambda: ta.dmi(high, low, close, 14),
            'parabolic_sar': lambda: ta.parabolic_sar(high, low, 0.02, 0.2),
            'psar': lambda: ta.psar(high, low, 0.02, 0.2),
            'pivot_points': lambda: ta.pivot_points(high, low, close),
            'fractals': lambda: ta.fractals(high, low),
            'zigzag': lambda: ta.zigzag(high, low, close, 5.0),
            'gator_oscillator': lambda: ta.gator_oscillator((high + low + close) / 3),
            'mode': lambda: ta.mode(close, 20),
            'uo_oscillator': lambda: ta.uo_oscillator(high, low, close),
            
            # Utility Functions (4)
            'crossover': lambda: ta.crossover(close, sma20),
            'crossunder': lambda: ta.crossunder(close, sma20),
            'highest': lambda: ta.highest(close, 20),
            'lowest': lambda: ta.lowest(close, 20),
            'change': lambda: ta.change(close, 20),
        }
        
        # Run benchmarks
        results = {}
        success_count = 0
        total_time = 0.0
        
        print(f"Benchmarking {len(indicator_tests)} indicators...")
        
        for name, test_func in indicator_tests.items():
            exec_time, error = benchmark_indicator(name, test_func)
            
            if exec_time is not None:
                results[name] = {
                    'time': exec_time,
                    'time_ms': exec_time * 1000,
                    'status': 'success'
                }
                success_count += 1
                total_time += exec_time
            else:
                results[name] = {
                    'time': None,
                    'time_ms': None,
                    'status': 'failed',
                    'error': error
                }
        
        all_results[size] = {
            'results': results,
            'summary': {
                'total_indicators': len(indicator_tests),
                'successful': success_count,
                'failed': len(indicator_tests) - success_count,
                'success_rate': (success_count / len(indicator_tests)) * 100,
                'total_time': total_time,
                'avg_time_ms': (total_time * 1000 / success_count) if success_count > 0 else 0
            }
        }
        
        print(f"✅ Completed: {success_count}/{len(indicator_tests)} successful")
        print(f"⏱️  Total time: {total_time:.3f}s")
        print(f"📊 Average: {all_results[size]['summary']['avg_time_ms']:.2f}ms per indicator")
    
    return all_results

def generate_markdown_report(results):
    """Generate the speed.md report with actual benchmark data"""
    
    report = []
    report.append("# OpenAlgo Technical Indicators - Speed Benchmark Report")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    report.append("Comprehensive performance benchmarks for all 103 technical indicators in the OpenAlgo library, tested across three dataset sizes: 1,000, 10,000, and 100,000 data points.")
    report.append("")
    
    # Summary table
    report.append("## Performance Overview")
    report.append("")
    report.append("| Dataset Size | Success Rate | Total Time | Avg Time/Indicator | Fastest | Slowest |")
    report.append("|-------------|--------------|------------|-------------------|---------|---------|")
    
    for size in [1000, 10000, 100000]:
        summary = results[size]['summary']
        successful_times = [r['time_ms'] for r in results[size]['results'].values() if r['status'] == 'success']
        fastest = min(successful_times) if successful_times else 0
        slowest = max(successful_times) if successful_times else 0
        
        report.append(f"| {size:,} points | {summary['success_rate']:.1f}% | {summary['total_time']:.3f}s | {summary['avg_time_ms']:.2f}ms | {fastest:.3f}ms | {slowest:.1f}ms |")
    
    report.append("")
    report.append("## Detailed Performance Results")
    report.append("")
    
    # Get all indicator names
    all_indicators = list(results[1000]['results'].keys())
    all_indicators.sort()
    
    # Group indicators by category
    categories = {
        'Trend': ['sma', 'ema', 'wma', 'dema', 'tema', 'hma', 'vwma', 'alma', 'kama', 'zlema', 
                  't3', 'frama', 'trima', 'vidya', 'mcginley', 'supertrend', 'ichimoku', 'alligator', 'ma_envelopes'],
        'Momentum': ['rsi', 'macd', 'stochastic', 'cci', 'williams_r', 'ultimate_oscillator', 'crsi', 'fisher', 'elderray'],
        'Volatility': ['bbands', 'atr', 'natr', 'true_range', 'keltner', 'donchian', 'bbpercent', 'bbwidth',
                       'starc', 'ulcerindex', 'hv', 'chandelier_exit', 'massindex', 'chaikin', 'rvol', 'rvi', 'vi', 'rwi'],
        'Volume': ['obv', 'vwap', 'mfi', 'adl', 'cmf', 'kvo', 'emv', 'force_index', 'nvi', 'pvi', 'pvt', 'volosc', 'vroc'],
        'Oscillators': ['roc', 'cmo', 'trix', 'ppo', 'po', 'dpo', 'awesome_oscillator', 'accelerator_oscillator',
                        'stochrsi', 'tsi', 'chop', 'aroon', 'aroon_oscillator', 'bop', 'ht', 'cho', 'ckstop',
                        'roc_oscillator', 'kst', 'stc'],
        'Statistical': ['linreg', 'lrslope', 'correlation', 'beta', 'variance', 'stdev', 'stddev', 'tsf', 'median'],
        'Hybrid': ['adx', 'dmi', 'parabolic_sar', 'psar', 'pivot_points', 'fractals', 'zigzag', 
                   'gator_oscillator', 'mode', 'uo_oscillator'],
        'Utility': ['crossover', 'crossunder', 'highest', 'lowest', 'change']
    }
    
    for category, indicators in categories.items():
        report.append(f"### {category} Indicators")
        report.append("")
        report.append("| Indicator | 1K (ms) | 10K (ms) | 100K (ms) | Scaling Ratio | Status |")
        report.append("|-----------|---------|----------|-----------|---------------|---------|")
        
        for indicator in indicators:
            if indicator in all_indicators:
                time_1k = results[1000]['results'][indicator]['time_ms']
                time_10k = results[10000]['results'][indicator]['time_ms']
                time_100k = results[100000]['results'][indicator]['time_ms']
                status_1k = results[1000]['results'][indicator]['status']
                
                if status_1k == 'success' and time_1k and time_1k > 0:
                    scaling = time_100k / time_1k
                    status = "✅"
                    report.append(f"| {indicator} | {time_1k:.3f} | {time_10k:.3f} | {time_100k:.3f} | {scaling:.1f}x | {status} |")
                else:
                    report.append(f"| {indicator} | - | - | - | - | ❌ |")
        report.append("")
    
    # Add performance analysis
    report.append("## Performance Analysis")
    report.append("")
    report.append("### Scaling Characteristics")
    report.append("")
    
    # Calculate scaling for successful indicators
    scaling_data = []
    for indicator in all_indicators:
        if results[1000]['results'][indicator]['status'] == 'success':
            time_1k = results[1000]['results'][indicator]['time_ms']
            time_100k = results[100000]['results'][indicator]['time_ms']
            if time_1k and time_1k > 0:
                scaling = time_100k / time_1k
                scaling_data.append((indicator, scaling, time_1k, time_100k))
    
    scaling_data.sort(key=lambda x: x[1])
    
    report.append("#### Best Scaling Indicators (Linear or Better)")
    report.append("")
    report.append("| Indicator | Scaling | 1K→100K |")
    report.append("|-----------|---------|---------|")
    for indicator, scaling, t1k, t100k in scaling_data[:10]:
        report.append(f"| {indicator} | {scaling:.1f}x | {t1k:.3f}ms→{t100k:.3f}ms |")
    report.append("")
    
    report.append("#### Indicators Needing Optimization (>100x scaling)")
    report.append("")
    report.append("| Indicator | Scaling | 1K→100K |")
    report.append("|-----------|---------|---------|")
    worst_scaling = [x for x in scaling_data if x[1] > 100]
    if worst_scaling:
        for indicator, scaling, t1k, t100k in worst_scaling:
            report.append(f"| {indicator} | {scaling:.1f}x | {t1k:.3f}ms→{t100k:.3f}ms |")
    else:
        report.append("| None | - | All indicators have good scaling |")
    report.append("")
    
    # Add timestamp
    from datetime import datetime
    report.append("---")
    report.append(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    report.append(f"*OpenAlgo version: 1.0.25*")
    
    return "\n".join(report)

if __name__ == "__main__":
    # Run benchmarks
    print("Starting comprehensive benchmark...")
    results = run_comprehensive_benchmark()
    
    # Generate report
    print("\nGenerating speed.md report...")
    report = generate_markdown_report(results)
    
    # Save report
    with open('speed.md', 'w') as f:
        f.write(report)
    
    print("\n✅ Benchmark complete! Report saved to speed.md")
    
    # Save raw results as JSON for reference
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("📊 Raw results saved to benchmark_results.json")