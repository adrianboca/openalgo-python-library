"""
Example of using OpenAlgo strategy with TradingView webhook
"""

from openalgo.strategy import Strategy, strategyorder

# Initialize webhook with your OpenAlgo server URL and webhook ID
webhook = Strategy(
    host_url="http://127.0.0.1:5000",  # Your OpenAlgo server URL
    webhook_id="your-webhook-id"        # Get this from OpenAlgo strategy section
)

# Example 1: Long/Short only mode (configured in OpenAlgo)
strategyorder(webhook, "RELIANCE", "BUY")

# Example 2: Both mode with position size
strategyorder(webhook, "ZOMATO", "SELL", 10)
