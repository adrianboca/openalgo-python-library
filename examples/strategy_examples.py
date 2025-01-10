"""
Example of using OpenAlgo strategy with client instance
"""

from openalgo import Strategy

# Initialize client with your OpenAlgo server URL and webhook ID
client = Strategy(
    host_url="http://127.0.0.1:5000",  # Your OpenAlgo server URL
    webhook_id="your-webhook-id"        # Get this from OpenAlgo strategy section
)

# Example 1: Long/Short only mode (configured in OpenAlgo)
client.strategyorder("RELIANCE", "BUY")

# Example 2: Both mode with position size
client.strategyorder("ZOMATO", "SELL", 10)

# You can also create multiple strategy instances if needed
another_strategy = Strategy(
    host_url="http://127.0.0.1:5000",
    webhook_id="another-webhook-id"
)

# The first initialized Strategy becomes the default for strategyorder()
