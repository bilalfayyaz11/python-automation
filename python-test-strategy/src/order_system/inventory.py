from typing import Dict, Optional

from .models import Product


class InventoryManager:
    def __init__(self):
        self.products: Dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        """Add a product to inventory."""
        self.products[product.id] = product

    def get_product(self, product_id: str) -> Optional[Product]:
        """Retrieve a product by ID."""
        return self.products.get(product_id)

    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Check if requested quantity is available."""
        product = self.get_product(product_id)

        if product is None:
            return False

        return product.stock >= quantity

    def reduce_stock(self, product_id: str, quantity: int) -> bool:
        """Reduce stock after order placement."""
        if not self.check_availability(product_id, quantity):
            return False

        product = self.products[product_id]
        product.stock -= quantity
        return True
