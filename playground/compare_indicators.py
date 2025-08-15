#!/usr/bin/env python
"""
Compare ADX with other technical indicators using real data
"""

import sys
import os

# Add the parent directory to path to use our current testing version
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openalgo import api
from openalgo import ta
import pandas as pd
import numpy as np

def compare_adx_with_indicators():
    """Compare ADX with RSI, MACD and other trend indicators"""
    
    print("Comparing ADX with Other Indicators")
    print("=" * 50)
    
    # Initialize API client
    client = api(
        api_key='91300b85a12a7c3c5c7fb091b6a8f17f94222a41a339d3e76640cf9bf4831350', 
        host='http://127.0.0.1:5001'
    )
    
    try:
        # Fetch data for multiple symbols
        symbols = ["RELIANCE", "TCS", "INFY"]
        
        for symbol in symbols:
            print(f"\n{'-'*20} {symbol} {'-'*20}")
            
            df = client.history(
                symbol=symbol, 
                exchange="NSE", 
                interval="D", 
                start_date="2024-01-01", 
                end_date="2025-01-14"
            )
            
            print(f"Data points: {len(df)}")
            
            # Calculate multiple indicators
            df['adx_plus'], df['adx_minus'], df['adx'] = ta.adx(df['high'], df['low'], df['close'], period=14)
            df['rsi'] = ta.rsi(df['close'], period=14)
            df['macd'], df['macd_signal'], df['macd_hist'] = ta.macd(df['close'])
            df['sma_20'] = ta.sma(df['close'], period=20)
            df['sma_50'] = ta.sma(df['close'], period=50)
            
            # Calculate trend strength correlation
            valid_data = df.dropna()
            
            if len(valid_data) > 50:
                # Identify strong trend periods
                strong_trend = valid_data[valid_data['adx'] > 25]
                weak_trend = valid_data[valid_data['adx'] < 20]
                
                print(f"Strong trend periods (ADX > 25): {len(strong_trend)} ({len(strong_trend)/len(valid_data)*100:.1f}%)")
                print(f"Weak trend periods (ADX < 20): {len(weak_trend)} ({len(weak_trend)/len(valid_data)*100:.1f}%)")
                
                if len(strong_trend) > 0:
                    print(f"Average ADX during strong trends: {strong_trend['adx'].mean():.2f}")
                    print(f"Price change during strong trends: {((strong_trend['close'].iloc[-1] / strong_trend['close'].iloc[0]) - 1) * 100:.2f}%")
                
                # Show recent analysis
                recent = valid_data.tail(10)
                print(f"\nRecent 10 days analysis:")
                analysis_cols = ['close', 'adx', 'adx_plus', 'adx_minus', 'rsi']
                print(recent[analysis_cols].round(2))
                
                # Trend signals
                latest = recent.iloc[-1]
                print(f"\nLatest signals for {symbol}:")
                print(f"ADX: {latest['adx']:.2f} ({'Strong' if latest['adx'] > 25 else 'Weak'} trend)")
                print(f"DI+: {latest['adx_plus']:.2f}, DI-: {latest['adx_minus']:.2f}")
                
                if latest['adx_plus'] > latest['adx_minus']:
                    print(f"Direction: Bullish (DI+ > DI-)")
                else:
                    print(f"Direction: Bearish (DI- > DI+)")
                    
                print(f"RSI: {latest['rsi']:.2f} ({'Overbought' if latest['rsi'] > 70 else 'Oversold' if latest['rsi'] < 30 else 'Neutral'})")
                
    except Exception as e:
        print(f"Error with real data: {e}")
        print("Testing with sample data instead...")
        test_sample_comparison()

def test_sample_comparison():
    """Test comparison with generated sample data"""
    
    print("\nTesting with sample data...")
    
    # Generate trending and sideways market data
    np.random.seed(42)
    
    # Create trending period
    trend_days = 50
    trend_returns = np.random.normal(0.01, 0.015, trend_days)  # Upward trend
    
    # Create sideways period  
    sideways_days = 50
    sideways_returns = np.random.normal(0, 0.01, sideways_days)  # No trend
    
    # Combine
    all_returns = np.concatenate([trend_returns, sideways_returns])
    base_price = 2500
    closes = base_price * np.exp(np.cumsum(all_returns))
    
    # Generate OHLC
    n = len(closes)
    spreads = np.random.uniform(0.005, 0.02, n)
    highs = closes * (1 + spreads/2)
    lows = closes * (1 - spreads/2)
    
    # Create DataFrame
    dates = pd.date_range('2024-01-01', periods=n, freq='D')
    df = pd.DataFrame({
        'high': highs,
        'low': lows,
        'close': closes
    }, index=dates)
    
    # Calculate indicators
    df['adx_plus'], df['adx_minus'], df['adx'] = ta.adx(df['high'], df['low'], df['close'], period=14)
    df['rsi'] = ta.rsi(df['close'], period=14)
    
    # Analyze periods
    trending_period = df.iloc[30:80]  # Skip warm-up period
    sideways_period = df.iloc[80:]
    
    trend_adx = trending_period['adx'].dropna()
    sideways_adx = sideways_period['adx'].dropna()
    
    print(f"\nTrending period ADX: {trend_adx.mean():.2f} (avg)")
    print(f"Sideways period ADX: {sideways_adx.mean():.2f} (avg)")
    
    print(f"\nExpected: Trending period should have higher ADX")
    print(f"Result: {'✓ Correct' if trend_adx.mean() > sideways_adx.mean() else '✗ Unexpected'}")
    
    # Show sample data
    print(f"\nSample results:")
    sample_cols = ['close', 'adx', 'adx_plus', 'adx_minus', 'rsi']
    print(df[sample_cols].tail(10).round(2))

if __name__ == "__main__":
    compare_adx_with_indicators()