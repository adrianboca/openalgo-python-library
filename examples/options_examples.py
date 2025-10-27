"""
OpenAlgo Options API Examples

This file demonstrates how to use the new Options API functions:
1. optiongreeks - Calculate Option Greeks and IV
2. optionsymbol - Get option symbol details
3. optionsorder - Place option orders with auto-resolved symbols
"""

import openalgo

# Initialize the API client
# Replace with your actual API key and host
api = openalgo.api(
    api_key="your_api_key_here",
    host="http://127.0.0.1:5000"
)

print("=" * 80)
print("OpenAlgo Options API Examples")
print("=" * 80)

# ============================================================================
# Example 1: Calculate Option Greeks (Basic)
# ============================================================================
print("\n1. Calculate Option Greeks - Basic Usage")
print("-" * 80)

greeks = api.optiongreeks(
    symbol="NIFTY28NOV2526000CE",
    exchange="NFO"
)

if greeks.get('status') == 'success':
    print(f"Symbol: {greeks['symbol']}")
    print(f"Underlying: {greeks['underlying']}")
    print(f"Strike: {greeks['strike']}")
    print(f"Spot Price: ₹{greeks['spot_price']}")
    print(f"Option Price: ₹{greeks['option_price']}")
    print(f"Days to Expiry: {greeks['days_to_expiry']}")
    print(f"Implied Volatility: {greeks['implied_volatility']}%")
    print(f"\nGreeks:")
    print(f"  Delta: {greeks['greeks']['delta']}")
    print(f"  Gamma: {greeks['greeks']['gamma']}")
    print(f"  Theta: {greeks['greeks']['theta']}")
    print(f"  Vega: {greeks['greeks']['vega']}")
    print(f"  Rho: {greeks['greeks']['rho']}")
else:
    print(f"Error: {greeks.get('message')}")

# ============================================================================
# Example 2: Calculate Option Greeks with Custom Interest Rate
# ============================================================================
print("\n\n2. Calculate Option Greeks - With Custom Interest Rate")
print("-" * 80)

greeks = api.optiongreeks(
    symbol="BANKNIFTY28NOV2550000CE",
    exchange="NFO",
    interest_rate=6.5  # Current RBI repo rate
)

if greeks.get('status') == 'success':
    print(f"Symbol: {greeks['symbol']}")
    print(f"Interest Rate Used: {greeks['interest_rate']}%")
    print(f"Implied Volatility: {greeks['implied_volatility']}%")
    print(f"Rho: {greeks['greeks']['rho']} (affected by interest rate)")
else:
    print(f"Error: {greeks.get('message')}")

# ============================================================================
# Example 3: Calculate Option Greeks Using Futures as Underlying
# ============================================================================
print("\n\n3. Calculate Option Greeks - Using Futures as Underlying")
print("-" * 80)

greeks = api.optiongreeks(
    symbol="NIFTY28NOV2526000CE",
    exchange="NFO",
    underlying_symbol="NIFTY28NOV25FUT",
    underlying_exchange="NFO"
)

if greeks.get('status') == 'success':
    print(f"Symbol: {greeks['symbol']}")
    print(f"Underlying: {greeks['underlying']} (Futures)")
    print(f"Futures Price: ₹{greeks['spot_price']}")
    print(f"Delta: {greeks['greeks']['delta']}")
else:
    print(f"Error: {greeks.get('message')}")

# ============================================================================
# Example 4: Calculate Option Greeks for MCX with Custom Expiry Time
# ============================================================================
print("\n\n4. Calculate Option Greeks - MCX with Custom Expiry Time")
print("-" * 80)

greeks = api.optiongreeks(
    symbol="CRUDEOIL17NOV255400CE",
    exchange="MCX",
    expiry_time="19:00"  # Crude Oil expires at 7:00 PM
)

if greeks.get('status') == 'success':
    print(f"Symbol: {greeks['symbol']}")
    print(f"Exchange: {greeks['exchange']}")
    print(f"Days to Expiry: {greeks['days_to_expiry']}")
    print(f"Implied Volatility: {greeks['implied_volatility']}%")
else:
    print(f"Error: {greeks.get('message')}")

# ============================================================================
# Example 5: Get Option Symbol Details
# ============================================================================
print("\n\n5. Get Option Symbol Details - ATM Call")
print("-" * 80)

symbol_info = api.optionsymbol(
    strategy="test_strategy",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=50,
    offset="ATM",
    option_type="CE"
)

if symbol_info.get('status') == 'success':
    print(f"Symbol: {symbol_info['symbol']}")
    print(f"Exchange: {symbol_info['exchange']}")
    print(f"Lot Size: {symbol_info['lotsize']}")
    print(f"Tick Size: {symbol_info['tick_size']}")
    print(f"Underlying LTP: ₹{symbol_info['underlying_ltp']}")
else:
    print(f"Error: {symbol_info.get('message')}")

# ============================================================================
# Example 6: Get Option Symbol Details - OTM Put
# ============================================================================
print("\n\n6. Get Option Symbol Details - OTM Put")
print("-" * 80)

symbol_info = api.optionsymbol(
    underlying="BANKNIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=100,
    offset="OTM2",
    option_type="PE"
)

if symbol_info.get('status') == 'success':
    print(f"Symbol: {symbol_info['symbol']}")
    print(f"Lot Size: {symbol_info['lotsize']}")
    print(f"Underlying LTP: ₹{symbol_info['underlying_ltp']}")
else:
    print(f"Error: {symbol_info.get('message')}")

# ============================================================================
# Example 7: Place Option Order - ATM Call (MARKET)
# ============================================================================
print("\n\n7. Place Option Order - ATM Call (MARKET)")
print("-" * 80)

order_result = api.optionsorder(
    strategy="test_strategy",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=50,
    offset="ATM",
    option_type="CE",
    action="BUY",
    quantity=75,
    price_type="MARKET",
    product="MIS"
)

if order_result.get('status') == 'success':
    print(f"Order ID: {order_result['orderid']}")
    print(f"Symbol: {order_result['symbol']}")
    print(f"Offset: {order_result['offset']}")
    print(f"Underlying LTP: ₹{order_result['underlying_ltp']}")
    if 'mode' in order_result:
        print(f"Mode: {order_result['mode']} (Analyze/Sandbox Mode)")
else:
    print(f"Error: {order_result.get('message')}")

# ============================================================================
# Example 8: Place Option Order - LIMIT Order
# ============================================================================
print("\n\n8. Place Option Order - LIMIT Order")
print("-" * 80)

order_result = api.optionsorder(
    strategy="nifty_scalping",
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=50,
    offset="OTM1",
    option_type="CE",
    action="BUY",
    quantity=75,
    price_type="LIMIT",
    product="MIS",
    price="50.0"
)

if order_result.get('status') == 'success':
    print(f"Order ID: {order_result['orderid']}")
    print(f"Symbol: {order_result['symbol']}")
    print(f"Order Type: LIMIT at ₹50.00")
else:
    print(f"Error: {order_result.get('message')}")

# ============================================================================
# Example 9: Place Option Order - Stop Loss Order
# ============================================================================
print("\n\n9. Place Option Order - Stop Loss Order")
print("-" * 80)

order_result = api.optionsorder(
    strategy="protective_stop",
    underlying="BANKNIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=100,
    offset="ATM",
    option_type="PE",
    action="SELL",
    quantity=30,
    price_type="SL",
    product="MIS",
    price="100.0",
    trigger_price="105.0"
)

if order_result.get('status') == 'success':
    print(f"Order ID: {order_result['orderid']}")
    print(f"Symbol: {order_result['symbol']}")
    print(f"Stop Loss Order: Trigger at ₹105, Limit at ₹100")
else:
    print(f"Error: {order_result.get('message')}")

# ============================================================================
# Example 10: Build an Iron Condor Strategy
# ============================================================================
print("\n\n10. Build Iron Condor Strategy - Get All 4 Symbols")
print("-" * 80)

# Leg 1: Sell OTM1 Call
leg1 = api.optionsymbol(
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=50,
    offset="OTM1",
    option_type="CE"
)

# Leg 2: Sell OTM1 Put
leg2 = api.optionsymbol(
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=50,
    offset="OTM1",
    option_type="PE"
)

# Leg 3: Buy OTM3 Call
leg3 = api.optionsymbol(
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=50,
    offset="OTM3",
    option_type="CE"
)

# Leg 4: Buy OTM3 Put
leg4 = api.optionsymbol(
    underlying="NIFTY",
    exchange="NSE_INDEX",
    expiry_date="28NOV24",
    strike_int=50,
    offset="OTM3",
    option_type="PE"
)

print("Iron Condor Strategy:")
print(f"  Sell OTM1 Call: {leg1.get('symbol', 'Error')}")
print(f"  Sell OTM1 Put:  {leg2.get('symbol', 'Error')}")
print(f"  Buy OTM3 Call:  {leg3.get('symbol', 'Error')}")
print(f"  Buy OTM3 Put:   {leg4.get('symbol', 'Error')}")

print("\n" + "=" * 80)
print("Examples completed!")
print("=" * 80)
