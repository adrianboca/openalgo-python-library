# -*- coding: utf-8 -*-
"""
OpenAlgo REST API Documentation - Options Methods
    https://docs.openalgo.in
"""

import httpx
from .base import BaseAPI

class OptionsAPI(BaseAPI):
    """
    Options API methods for OpenAlgo.
    Inherits from the BaseAPI class.
    """

    def _make_request(self, endpoint, payload):
        """Make HTTP request with proper error handling"""
        url = self.base_url + endpoint
        try:
            response = httpx.post(url, json=payload, headers=self.headers, timeout=self.timeout)
            return self._handle_response(response)
        except httpx.TimeoutException:
            return {
                'status': 'error',
                'message': 'Request timed out. The server took too long to respond.',
                'error_type': 'timeout_error'
            }
        except httpx.ConnectError:
            return {
                'status': 'error',
                'message': 'Failed to connect to the server. Please check if the server is running.',
                'error_type': 'connection_error'
            }
        except httpx.HTTPError as e:
            return {
                'status': 'error',
                'message': f'HTTP error occurred: {str(e)}',
                'error_type': 'http_error'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'An unexpected error occurred: {str(e)}',
                'error_type': 'unknown_error'
            }

    def _handle_response(self, response):
        """Helper method to handle API responses"""
        try:
            if response.status_code != 200:
                return {
                    'status': 'error',
                    'message': f'HTTP {response.status_code}: {response.text}',
                    'code': response.status_code,
                    'error_type': 'http_error'
                }

            data = response.json()
            if data.get('status') == 'error':
                return {
                    'status': 'error',
                    'message': data.get('message', 'Unknown error'),
                    'code': response.status_code,
                    'error_type': 'api_error'
                }
            return data

        except ValueError:
            return {
                'status': 'error',
                'message': 'Invalid JSON response from server',
                'raw_response': response.text,
                'error_type': 'json_error'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'error_type': 'unknown_error'
            }

    def optiongreeks(self, *, symbol, exchange, interest_rate=None, underlying_symbol=None, underlying_exchange=None, expiry_time=None):
        """
        Calculate Option Greeks (Delta, Gamma, Theta, Vega, Rho) and Implied Volatility using Black-Scholes Model.

        Prerequisites:
        - mibian library required: pip install mibian
        - Requires real-time LTP for underlying and option

        Parameters:
        - symbol (str): Option symbol (e.g., NIFTY28NOV2526000CE). Required.
        - exchange (str): Exchange code (NFO, BFO, CDS, MCX). Required.
        - interest_rate (float, optional): Risk-free interest rate (annualized %).
                                          Default is 0. Specify current RBI repo rate (e.g., 6.5)
                                          for accurate Rho calculations.
        - underlying_symbol (str, optional): Custom underlying symbol (e.g., NIFTY or NIFTY28NOV25FUT).
                                            Auto-detected if not specified.
        - underlying_exchange (str, optional): Custom underlying exchange (e.g., NSE_INDEX or NFO).
                                              Auto-detected if not specified.
        - expiry_time (str, optional): Custom expiry time in HH:MM format (e.g., "17:00", "19:00").
                                      Required for MCX contracts with non-standard expiry times.
                                      Exchange defaults: NFO/BFO=15:30, CDS=12:30, MCX=23:30

        Returns:
        dict: JSON response containing:
            - status: success/error
            - symbol: Option symbol
            - exchange: Exchange code
            - underlying: Underlying symbol
            - strike: Strike price
            - option_type: CE/PE
            - expiry_date: Expiry date
            - days_to_expiry: Days remaining to expiry
            - spot_price: Underlying price
            - option_price: Current option premium
            - interest_rate: Interest rate used
            - implied_volatility: Implied Volatility (%)
            - greeks: Object containing Delta, Gamma, Theta, Vega, Rho

        Example:
            # Basic usage with auto-detected spot
            greeks = api.optiongreeks(
                symbol="NIFTY28NOV2526000CE",
                exchange="NFO"
            )

            # With custom interest rate
            greeks = api.optiongreeks(
                symbol="BANKNIFTY28NOV2550000CE",
                exchange="NFO",
                interest_rate=6.5
            )

            # Using futures as underlying
            greeks = api.optiongreeks(
                symbol="NIFTY28NOV2526000CE",
                exchange="NFO",
                underlying_symbol="NIFTY28NOV25FUT",
                underlying_exchange="NFO"
            )

            # MCX with custom expiry time
            greeks = api.optiongreeks(
                symbol="CRUDEOIL17NOV255400CE",
                exchange="MCX",
                expiry_time="19:00"
            )
        """
        payload = {
            "apikey": self.api_key,
            "symbol": symbol,
            "exchange": exchange
        }

        # Add optional parameters if provided
        if interest_rate is not None:
            payload["interest_rate"] = interest_rate
        if underlying_symbol is not None:
            payload["underlying_symbol"] = underlying_symbol
        if underlying_exchange is not None:
            payload["underlying_exchange"] = underlying_exchange
        if expiry_time is not None:
            payload["expiry_time"] = expiry_time

        return self._make_request("optiongreeks", payload)

    def optionsorder(self, *, strategy="Python", underlying, exchange, strike_int, offset, option_type, action, quantity, expiry_date=None, price_type="MARKET", product="MIS", **kwargs):
        """
        Place Option Orders by Auto-Resolving Symbol based on Underlying and Offset.

        Parameters:
        - strategy (str, optional): Strategy name. Defaults to "Python".
        - underlying (str): Underlying symbol (e.g., NIFTY, BANKNIFTY, NIFTY28OCT25FUT). Required.
        - exchange (str): Exchange code (NSE_INDEX, NSE, NFO, BSE_INDEX, BSE, BFO). Required.
        - strike_int (int): Strike interval (50 for NIFTY, 100 for BANKNIFTY). Required.
        - offset (str): Strike offset (ATM, ITM1-ITM50, OTM1-OTM50). Required.
        - option_type (str): Option type (CE for Call, PE for Put). Required.
        - action (str): BUY or SELL. Required.
        - quantity (int/str): Quantity (must be multiple of lot size). Required.
        - expiry_date (str, optional): Expiry date in DDMMMYY format (e.g., 28OCT25).
                                      Optional if underlying includes expiry (e.g., NIFTY28OCT25FUT).
        - price_type (str, optional): Price type (MARKET/LIMIT/SL/SL-M). Defaults to "MARKET".
        - product (str, optional): Product type (MIS/NRML). Defaults to "MIS".
                                  Note: Options only support MIS and NRML (CNC not supported).
        - **kwargs: Optional parameters like:
            - price (str): Required for LIMIT orders
            - trigger_price (str): Required for SL and SL-M orders
            - disclosed_quantity (str): Disclosed quantity

        Returns:
        dict: JSON response containing:
            - status: success/error
            - orderid: Broker order ID (or SB-xxx for analyze mode)
            - symbol: Resolved option symbol
            - exchange: Exchange code where order is placed
            - underlying: Underlying symbol from request
            - underlying_ltp: Last Traded Price of underlying
            - offset: Strike offset from request
            - option_type: CE/PE
            - mode: Trading mode (analyze/live) - only present in Analyze Mode

        Example:
            # Basic ATM call order
            result = api.optionsorder(
                strategy="test_strategy",
                underlying="NIFTY",
                exchange="NSE_INDEX",
                expiry_date="28NOV24",
                strike_int=50,
                offset="ATM",
                option_type="CE",
                action="BUY",
                quantity=75
            )

            # Using future as underlying
            result = api.optionsorder(
                strategy="test_strategy",
                underlying="NIFTY28OCT25FUT",
                exchange="NFO",
                strike_int=50,
                offset="ITM2",
                option_type="CE",
                action="BUY",
                quantity=75
            )

            # LIMIT order
            result = api.optionsorder(
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
                price="50.0"
            )
        """
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "underlying": underlying,
            "exchange": exchange,
            "strike_int": str(strike_int),
            "offset": offset,
            "option_type": option_type,
            "action": action,
            "quantity": str(quantity),
            "pricetype": price_type,
            "product": product
        }

        # Add expiry_date if provided
        if expiry_date is not None:
            payload["expiry_date"] = expiry_date

        # Convert numeric values to strings
        for key, value in kwargs.items():
            if value is not None:
                payload[key] = str(value)

        return self._make_request("optionsorder", payload)

    def optionsymbol(self, *, strategy="Python", underlying, exchange, strike_int, offset, option_type, expiry_date=None):
        """
        Returns Option Symbol Details based on Underlying and Offset.

        This function helps you get the exact option symbol, lot size, and tick size
        without placing an order. Useful for:
        - Verifying symbol exists before ordering
        - Getting lot size for quantity calculations
        - Building option strategies (Iron Condor, Straddle, etc.)
        - Getting current ATM strike

        Parameters:
        - strategy (str, optional): Strategy name. Defaults to "Python".
        - underlying (str): Underlying symbol (e.g., NIFTY, BANKNIFTY, NIFTY28OCT25FUT). Required.
        - exchange (str): Exchange code (NSE_INDEX, NSE, NFO, BSE_INDEX, BSE, BFO). Required.
        - strike_int (int): Strike interval (50 for NIFTY, 100 for BANKNIFTY). Required.
        - offset (str): Strike offset (ATM, ITM1-ITM50, OTM1-OTM50). Required.
        - option_type (str): Option type (CE for Call, PE for Put). Required.
        - expiry_date (str, optional): Expiry date in DDMMMYY format (e.g., 28OCT25).
                                      Optional if underlying includes expiry (e.g., NIFTY28OCT25FUT).

        Returns:
        dict: JSON response containing:
            - status: success/error
            - symbol: Resolved option symbol
            - exchange: Exchange code where option is listed
            - lotsize: Lot size of the option contract
            - tick_size: Minimum price movement
            - underlying_ltp: Last Traded Price of underlying

        Example:
            # Get ATM call symbol
            symbol_info = api.optionsymbol(
                strategy="test_strategy",
                underlying="NIFTY",
                exchange="NSE_INDEX",
                expiry_date="28OCT25",
                strike_int=50,
                offset="ATM",
                option_type="CE"
            )
            print(f"Symbol: {symbol_info['symbol']}")
            print(f"Lot Size: {symbol_info['lotsize']}")

            # Get OTM put for BANKNIFTY
            symbol_info = api.optionsymbol(
                underlying="BANKNIFTY",
                exchange="NSE_INDEX",
                expiry_date="28NOV24",
                strike_int=100,
                offset="OTM2",
                option_type="PE"
            )

            # Using future as underlying
            symbol_info = api.optionsymbol(
                underlying="NIFTY28OCT25FUT",
                exchange="NFO",
                strike_int=50,
                offset="ITM2",
                option_type="CE"
            )
        """
        payload = {
            "apikey": self.api_key,
            "strategy": strategy,
            "underlying": underlying,
            "exchange": exchange,
            "strike_int": str(strike_int),
            "offset": offset,
            "option_type": option_type
        }

        # Add expiry_date if provided
        if expiry_date is not None:
            payload["expiry_date"] = expiry_date

        return self._make_request("optionsymbol", payload)
