from typing import List, Tuple

from .inventory import InventoryManager
from .models import Order


class OrderProcessor:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory = inventory_manager
        self.processed_orders: List[Order] = []

    def validate_order(self, order: Order) -> Tuple[bool, str]:
        """
        Validate order items against inventory.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not order.items:
            return False, "Order must contain at least one item"

        for item in order.items:
            product_id = item.product.id

            if not self.inventory.check_availability(product_id, item.quantity):
                return (
                    False,
                    f"Insufficient stock or missing product: {product_id}",
                )

        return True, ""

    def process_order(self, order: Order) -> Tuple[bool, str]:
        """
        Process an order: validate and update inventory.

        Returns:
            Tuple of (success, message)
        """
        is_valid, error_message = self.validate_order(order)

        if not is_valid:
            return False, error_message

        for item in order.items:
            self.inventory.reduce_stock(item.product.id, item.quantity)

        self.processed_orders.append(order)
        return True, "Order processed successfully"
