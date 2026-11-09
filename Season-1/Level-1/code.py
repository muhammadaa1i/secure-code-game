'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple
from decimal import Decimal

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

MAX_ITEM_AMOUNT = Decimal('100000')  # largest single payment or price
MAX_QUANTITY = 100                    # largest quantity of one product
MAX_TOTAL = Decimal('1000000')        # largest total payable per order


def validorder(order: Order):
    payable = Decimal('0')
    paid = Decimal('0')

    for item in order.items:
        # Decimal(str(...)) avoids binary float rounding (1.1 + 2.2 != 3.3)
        amount = Decimal(str(item.amount))
        if item.type == 'payment':
            # Ignore out-of-range payments: huge pay-and-refund pairs
            # would otherwise swallow the price of a product.
            if -MAX_ITEM_AMOUNT <= amount <= MAX_ITEM_AMOUNT:
                paid += amount
        elif item.type == 'product':
            if (not 0 < amount <= MAX_ITEM_AMOUNT
                    or not 0 < item.quantity <= MAX_QUANTITY):
                return "Invalid product: %s" % item.description
            payable += amount * Decimal(str(item.quantity))
        else:
            return "Invalid item type: %s" % item.type

    if payable > MAX_TOTAL:
        return "Total amount payable for an order exceeded"

    net = paid - payable
    if net != 0:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net)
    else:
        return "Order ID: %s - Full payment received!" % order.id