"""
OpenAlgo Strategy Module for TradingView Integration
"""

from typing import Optional

class Strategy:
    def __init__(self, host_url: str, webhook_id: str):
        """
        Initialize strategy with host URL and webhook ID
        
        Args:
            host_url (str): OpenAlgo server URL (e.g., "http://127.0.0.1:5000")
            webhook_id (str): Strategy's webhook ID from OpenAlgo
        """
        self.webhook_url = f"{host_url.rstrip('/')}/strategy/webhook/{webhook_id}"

def strategyorder(webhook: Strategy, symbol: str, action: str, position_size: Optional[int] = None) -> dict:
    """
    Format the strategy order message for TradingView webhook.
    The strategy mode (LONG_ONLY, SHORT_ONLY, BOTH) is configured in OpenAlgo.
    
    Args:
        webhook (Strategy): Strategy instance with webhook configuration
        symbol (str): Trading symbol (e.g., "RELIANCE", "NIFTY")
        action (str): Order action ("BUY" or "SELL")
        position_size (Optional[int]): Position size, required for BOTH mode
        
    Returns:
        dict: Message format for TradingView webhook
    """
    message = {
        "symbol": symbol,
        "action": action.upper()
    }
    
    if position_size is not None:
        message["position_size"] = str(position_size)
        
    return message
