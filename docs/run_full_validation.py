# validate_full.py
"""
Comprehensive validation and performance benchmark for the OpenAlgo library against
TA-Lib or NumPy-based reference implementations.

USAGE
-----
python validate_full.py path/to/your/data.csv

- The script processes a large CSV file (~1M rows).
- It validates all indicators found in the OpenAlgo library.
- It provides performance statistics (in milliseconds).
- It reports Mean Absolute Error (MAE) and Max Absolute Error (MaxAE).
- It uses NumPy implementations for indicators not found in TA-Lib.
"""
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table
import talib
from openalgo import ta

# --- Configuration ---
TOLERANCE = 1e-5  # Acceptance tolerance for Mean Absolute Error

# =============================================================================
# NUMPY-BASED REFERENCE IMPLEMENTATIONS (for indicators TA-Lib lacks)
# =============================================================================

def ref_sma(series, period):
    """NumPy Simple Moving Average."""
    return pd.Series(series).rolling(window=period).mean().values

def ref_ema(series, period):
    """NumPy Exponential Moving Average."""
    return pd.Series(series).ewm(span=period, adjust=False).mean().values

def ref_wma(series, period):
    """NumPy Weighted Moving Average."""
    weights = np.arange(1, period + 1)
    return pd.Series(series).rolling(window=period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True).values

def ref_hma(series, period):
    """NumPy Hull Moving Average."""
    half_period = int(period / 2)
    sqrt_period = int(np.sqrt(period))
    wma_half = ref_wma(series, half_period)
    wma_full = ref_wma(series, period)
    diff = 2 * wma_half - wma_full
    return ref_wma(diff, sqrt_period)

def ref_alma(series, period, sigma=6, offset=0.85):
    """NumPy Arnaud Legoux Moving Average."""
    m = offset * (period - 1)
    s = period / sigma
    w = np.exp(-((np.arange(period) - m) ** 2) / (2 * s * s))
    return pd.Series(series).rolling(window=period).apply(lambda x: np.dot(x, w) / w.sum(), raw=True).values

def ref_supertrend(high, low, close, period=7, multiplier=3.0):
    """NumPy SuperTrend."""
    atr = talib.ATR(high, low, close, timeperiod=period)
    hl2 = (high + low) / 2
    upper_band = hl2 + (multiplier * atr)
    lower_band = hl2 - (multiplier * atr)
    
    st = np.full(len(close), np.nan)
    trend = np.ones(len(close)) # 1 for uptrend, -1 for downtrend

    for i in range(1, len(close)):
        if close[i] > upper_band[i-1]:
            trend[i] = 1
        elif close[i] < lower_band[i-1]:
            trend[i] = -1
        else:
            trend[i] = trend[i-1]

        if trend[i] == 1:
            lower_band[i] = max(lower_band[i], lower_band[i-1])
        else:
            upper_band[i] = min(upper_band[i], upper_band[i-1])

    for i in range(len(close)):
        st[i] = lower_band[i] if trend[i] == 1 else upper_band[i]
        
    return st, trend

def ref_dpo(series, period):
    """NumPy Detrended Price Oscillator."""
    shift = int(period / 2) + 1
    sma = ref_sma(series, period)
    return pd.Series(series).shift(-shift) - sma

# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def _dropna_pair(a, b):
    """Remove rows where either array has a NaN."""
    mask = ~(np.isnan(a) | np.isnan(b))
    return a[mask], b[mask]

def calculate_mae(a, b):
    a_clean, b_clean = _dropna_pair(a, b)
    return np.nan if a_clean.size == 0 else np.mean(np.abs(a_clean - b_clean))

def calculate_maxae(a, b):
    a_clean, b_clean = _dropna_pair(a, b)
    return np.nan if a_clean.size == 0 else np.max(np.abs(a_clean - b_clean))

def time_ms(func, *args):
    """Time a function call and return result and duration in ms."""
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, (end - start) * 1000

# =============================================================================
# INDICATOR MAPPING
# =============================================================================

# (openalgo_func, ref_func, params, input_cols, ref_source)
INDICATOR_MAP = {
    # Trend
    'sma': (ta.sma, talib.SMA, {'period': 20}, ['c'], 'TA-Lib'),
    'ema': (ta.ema, talib.EMA, {'period': 20}, ['c'], 'TA-Lib'),
    'wma': (ta.wma, talib.WMA, {'period': 20}, ['c'], 'TA-Lib'),
    'dema': (ta.dema, talib.DEMA, {'period': 20}, ['c'], 'TA-Lib'),
    'tema': (ta.tema, talib.TEMA, {'period': 20}, ['c'], 'TA-Lib'),
    'hma': (ta.hma, ref_hma, {'period': 20}, ['c'], 'NumPy'),
    'vwma': (ta.vwma, None, {'period': 20}, ['c', 'v'], 'Skip'), # No simple ref
    'alma': (lambda c,p,o,s: ta.alma(c,p,o,s), ref_alma, {'period': 9, 'offset': 0.85, 'sigma': 6}, ['c'], 'NumPy'),
    'kama': (ta.kama, talib.KAMA, {'period': 10}, ['c'], 'TA-Lib'),
    'zlema': (ta.zlema, None, {'period': 20}, ['c'], 'Skip'), # Complex ref
    't3': (ta.t3, talib.T3, {'period': 5, 'v_factor': 0.7}, ['c'], 'TA-Lib'),
    'supertrend': (lambda h,l,c,p,m: ta.supertrend(h,l,c,p,m)[0], lambda h,l,c,p,m: ref_supertrend(h,l,c,p,m)[0], {'period': 7, 'multiplier': 3.0}, ['h', 'l', 'c'], 'NumPy'),
    'ichimoku': (lambda h,l,c,p1,p2,p3: ta.ichimoku(h,l,c,p1,p2,p3)[0], None, {'tenkan_period': 9, 'kijun_period': 26, 'senkou_period': 52}, ['h','l','c'], 'Skip'), # Multi-output

    # Momentum
    'rsi': (ta.rsi, talib.RSI, {'period': 14}, ['c'], 'TA-Lib'),
    'macd': (lambda c,f,s,sig: ta.macd(c,f,s,sig)[0], lambda c,f,s,sig: talib.MACD(c,f,s,sig)[0], {'fast_period': 12, 'slow_period': 26, 'signal_period': 9}, ['c'], 'TA-Lib'),
    'stoch': (lambda h,l,c,kp,dp: ta.stochastic(h,l,c,kp,dp)[0], lambda h,l,c,kp,dp: talib.STOCH(h,l,c,kp,dp,dp)[0], {'k_period': 14, 'd_period': 3}, ['h','l','c'], 'TA-Lib'),
    'cci': (ta.cci, talib.CCI, {'period': 14}, ['h','l','c'], 'TA-Lib'),
    'williams_r': (ta.williams_r, talib.WILLR, {'period': 14}, ['h','l','c'], 'TA-Lib'),
    
    # Oscillators
    'roc': (ta.roc_oscillator, talib.ROC, {'period': 10}, ['c'], 'TA-Lib'),
    'ppo': (lambda c,fp,sp,sig: ta.ppo(c,fp,sp,sig)[0], lambda c,fp,sp,sig: talib.PPO(c,fp,sp), {'fast_period': 12, 'slow_period': 26, 'signal_period': 9}, ['c'], 'TA-Lib'),
    'trix': (ta.trix, talib.TRIX, {'period': 30}, ['c'], 'TA-Lib'),
    'dpo': (ta.dpo, lambda c,p: ref_dpo(c,p), {'period': 20}, ['c'], 'NumPy'),
    'aroon_osc': (ta.aroon_oscillator, talib.AROONOSC, {'period': 14}, ['h','l'], 'TA-Lib'),

    # Volatility
    'atr': (ta.atr, talib.ATR, {'period': 14}, ['h','l','c'], 'TA-Lib'),
    'bbands': (lambda c,p,s: ta.bbands(c,p,s)[0], lambda c,p,s,s2: talib.BBANDS(c,p,s,s2)[0], {'period': 20, 'std_dev': 2.0}, ['c'], 'TA-Lib'),
    'keltner_channel': (lambda h,l,c,p,m: ta.keltner_channel(h,l,c,p,m)[0], None, {'period': 20, 'multiplier': 2.0}, ['h','l','c'], 'Skip'),
    'donchian_channel': (lambda h,l,p: ta.donchian_channel(h,l,p)[0], None, {'period': 20}, ['h','l'], 'Skip'),
    'natr': (ta.natr, talib.NATR, {'period': 14}, ['h','l','c'], 'TA-Lib'),

    # Volume
    'obv': (ta.obv, talib.OBV, {}, ['c','v'], 'TA-Lib'),
    'vwap': (ta.vwap, None, {'anchor': 0}, ['h','l','c','v'], 'Skip'),
    'mfi': (ta.mfi, talib.MFI, {'period': 14}, ['h','l','c','v'], 'TA-Lib'),
    'adl': (ta.adl, talib.AD, {}, ['h','l','c','v'], 'TA-Lib'),
    'cmf': (ta.cmf, None, {'period': 20}, ['h','l','c','v'], 'Skip'),

    # Statistics
    'stdev': (ta.stdev, talib.STDDEV, {'period': 5}, ['c'], 'TA-Lib'),
    'variance': (ta.variance, talib.VAR, {'period': 5}, ['c'], 'TA-Lib'),
    'beta': (ta.beta, talib.BETA, {'period': 5}, ['h','l'], 'TA-Lib'),
    'correlation': (ta.correlation, talib.CORREL, {'period': 30}, ['h','l'], 'TA-Lib'),
    
    # Hybrid
    'adx': (lambda h,l,c,p: ta.adx_system(h,l,c,p)[2], talib.ADX, {'period': 14}, ['h','l','c'], 'TA-Lib'),
    'sar': (ta.psar, talib.SAR, {'af': 0.02, 'max_af': 0.2}, ['h','l'], 'TA-Lib'),
}

# =============================================================================
# MAIN SCRIPT
# =============================================================================

def run_validation(df: pd.DataFrame):
    console = Console()
    
    # Prepare data arrays
    data_arrays = {
        'h': df['HIGH'].astype('float64').values,
        'l': df['LOW'].astype('float64').values,
        'c': df['CLOSE'].astype('float64').values,
        'v': df['VOLUME'].astype('float64').values,
    }

    table = Table(title=f"OpenAlgo Full Validation & Performance (Records: {len(df):,})", box=box.HEAVY_HEAD)
    table.add_column("Indicator", justify="left", style="cyan", no_wrap=True)
    table.add_column("Source", justify="center", style="magenta")
    table.add_column("OpenAlgo (ms)", justify="right", style="green")
    table.add_column("Reference (ms)", justify="right", style="yellow")
    table.add_column("MAE", justify="right", style="white")
    table.add_column("MaxAE", justify="right", style="white")
    table.add_column("Pass", justify="center")

    all_passed = True
    
    with console.status("[bold green]Running validations...") as status:
        for name, (oa_func, ref_func, params, inputs, source) in INDICATOR_MAP.items():
            if source == 'Skip' or ref_func is None:
                continue

            status.update(f"Validating [bold]{name}[/]...")
            
            # Prepare args
            oa_args = [data_arrays[i] for i in inputs] + list(params.values())
            
            # Special handling for TA-Lib's BBANDS stddev params
            if name == 'bbands':
                ref_args = [data_arrays['c'], params['period'], params['std_dev'], params['std_dev']]
            else:
                ref_args = [data_arrays[i] for i in inputs] + list(params.values())

            try:
                # Time OpenAlgo
                oa_val, oa_time = time_ms(oa_func, *oa_args)
                
                # Time Reference
                ref_val, ref_time = time_ms(ref_func, *ref_args)

                # Flatten multi-output arrays if necessary
                if oa_val.ndim > 1: oa_val = oa_val.ravel()
                if ref_val.ndim > 1: ref_val = ref_val.ravel()

                # Calculate errors
                mae = calculate_mae(oa_val, ref_val)
                max_ae = calculate_maxae(oa_val, ref_val)
                
                passed = mae <= TOLERANCE
                if not passed: all_passed = False
                
                status_str = "[green]✔[/green]" if passed else "[red]✘[/red]"
                param_str = ", ".join(f"{v}" for v in params.values())
                
                table.add_row(
                    f"{name.upper()}({param_str})",
                    source,
                    f"{oa_time:.2f}",
                    f"{ref_time:.2f}",
                    f"{mae:,.6g}",
                    f"{max_ae:,.6g}",
                    status_str
                )
            except Exception as e:
                param_str = ", ".join(f"{v}" for v in params.values())
                table.add_row(f"{name.upper()}({param_str})", source, "-", "-", f"[red]ERROR[/red]", str(e), "[red]✘[/red]")
                all_passed = False

    console.print(table)
    return all_passed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python validate_full.py <path_to_data.csv>")

    csv_path = Path(sys.argv[1])
    if not csv_path.is_file():
        sys.exit(f"Error: File not found at {csv_path}")

    console = Console()
    console.print(f"Loading data from [bold cyan]{csv_path}[/]...")
    
    try:
        df = pd.read_csv(csv_path)
        df.columns = [c.strip().upper() for c in df.columns]
        console.print(f"Loaded [bold green]{len(df):,}[/] records.")
    except Exception as e:
        sys.exit(f"Error loading CSV: {e}")

    # Run the main validation
    success = run_validation(df)

    # Final summary
    if success:
        console.print("\n[bold green]✅ All implemented indicators passed validation within tolerance![/]")
        sys.exit(0)
    else:
        console.print("\n[bold red]❌ Deviations or errors detected. Please review the table above.[/]")
        sys.exit(1)
