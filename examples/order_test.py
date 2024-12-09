# -*- coding: utf-8 -*-
"""
OpenAlgo Order API Test Examples
"""

from openalgo import api
import time

def main():
    # Initialize API with test credentials
    client = api(
        api_key="38f99d7d226cc0c3baa19dcacf0b1f049d2f68371da1dda2c97b1b63a3a9ca2e",
        host="http://127.0.0.1:5000"
    )

    # Test 1: Place a regular order
    print("\nTest 1: Place Order")
    order_result = client.placeorder(
        symbol="YESBANK",
        exchange="NSE",
        action="BUY",
        quantity=10,
        price_type="MARKET",
        product="CNC"
    )
    print("Place Order Result:", order_result)

    if order_result.get('status') == 'success':
        order_id = order_result.get('orderid')

        # Test 2: Check order status
        print("\nTest 2: Order Status")
        status_result = client.orderstatus(
            order_id=order_id,
            strategy="Test Strategy"
        )
        print("Order Status Result:", status_result)

        # Test 3: Check open position
        print("\nTest 3: Open Position")
        position_result = client.openposition(
            strategy="Test Strategy",
            symbol="YESBANK",
            exchange="NSE",
            product="CNC"
        )
        print("Open Position Result:", position_result)

    # Test 4: Place a basket order
    print("\nTest 4: Basket Order")
    basket_orders = [
        {
            "symbol": "RELIANCE",
            "exchange": "NSE",
            "action": "BUY",
            "quantity": 1,
            "pricetype": "MARKET",
            "product": "MIS"
        },
        {
            "symbol": "INFY",
            "exchange": "NSE",
            "action": "SELL",
            "quantity": 1,
            "pricetype": "MARKET",
            "product": "MIS"
        }
    ]
    basket_result = client.basketorder(orders=basket_orders)
    print("Basket Order Result:", basket_result)

    # Test 5: Place a split order
    print("\nTest 5: Split Order")
    split_result = client.splitorder(
        symbol="YESBANK",
        exchange="NSE",
        action="SELL",
        quantity=105,
        splitsize=20,
        price_type="MARKET",
        product="MIS"
    )
    print("Split Order Result:", split_result)

    # Test 6: Place a smart order
    print("\nTest 6: Smart Order")
    smart_result = client.placesmartorder(
        symbol="YESBANK",
        exchange="NSE",
        action="BUY",
        quantity=10,
        position_size=100,
        price_type="MARKET",
        product="MIS"
    )
    print("Smart Order Result:", smart_result)

    # Test 7: Modify an order (if we have an order ID from previous tests)
    if order_result.get('status') == 'success':
        print("\nTest 7: Modify Order")
        modify_result = client.modifyorder(
            order_id=order_id,
            symbol="YESBANK",
            exchange="NSE",
            action="BUY",
            quantity=15,  # Modified quantity
            price="100",  # New price
            product="CNC",
            price_type="LIMIT"
        )
        print("Modify Order Result:", modify_result)

        # Test 8: Cancel specific order
        print("\nTest 8: Cancel Order")
        cancel_result = client.cancelorder(order_id=order_id)
        print("Cancel Order Result:", cancel_result)

    # Test 9: Cancel all orders
    print("\nTest 9: Cancel All Orders")
    cancel_all_result = client.cancelallorder()
    print("Cancel All Orders Result:", cancel_all_result)

    # Test 10: Close all positions
    print("\nTest 10: Close Positions")
    close_result = client.closeposition()
    print("Close Positions Result:", close_result)

if __name__ == "__main__":
    main()
