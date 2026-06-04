from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Product:
    id: str
    name: str
    price: Decimal
    stock: int


@dataclass
class OrderItem:
    product: Product
    quantity: int

    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this order item."""
        return self.product.price * self.quantity


@dataclass
class Order:
    order_id: str
    items: List[OrderItem]
    discount_percent: Decimal = Decimal("0")

    def calculate_total(self) -> Decimal:
        """Calculate order total with discount applied."""
        subtotal = sum(item.get_subtotal() for item in self.items)

        if self.discount_percent <= 0:
            return subtotal

        discount_amount = subtotal * (self.discount_percent / Decimal("100"))
        return subtotal - discount_amount
