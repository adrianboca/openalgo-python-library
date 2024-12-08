# OpenAlgo Examples

This directory contains example scripts demonstrating the usage of OpenAlgo's Python API.

## Setup

Before running the examples, you need to install the openalgo package in development mode. From the root directory of the project:

```bash
# Activate your virtual environment if you haven't already
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows

# Install the package in development mode
pip install -e .
```

## Running Examples

After installation, you can run any of the example scripts:

```bash
# Run order management examples
python examples/order_examples.py

# Run market data examples
python examples/data_examples.py
```

## Available Examples

1. `order_examples.py` - Demonstrates order management functionality:
   - Place regular orders
   - Place smart orders
   - Modify orders
   - Cancel orders
   - Close positions
   - Cancel all orders

2. `data_examples.py` - Demonstrates market data functionality:
   - Get real-time quotes
   - Get market depth
   - Get historical data
   - Get supported intervals
   - Combined market data example

## API Key

The examples use the following API configuration:
```python
api_key = "38f99d7d226cc0c3baa19dcacf0b1f049d2f68371da1dda2c97b1b63a3a9ca2e"
host = "http://127.0.0.1:5000"
```

Make sure your OpenAlgo server is running at the specified host before running the examples.
