import pytest
from decimal import Decimal

from src.order_system.inventory import InventoryManager
from src.order_system.models import Order, OrderItem, Product
from src.order_system.processor import OrderProcessor


@pytest.mark.integration
class TestOrderProcessingIntegration:
    """Integration tests for complete order processing workflow."""

    @pytest.fixture
    def setup_system(self):
        """Fixture setting up complete system with inventory."""
        inventory = InventoryManager()
        processor = OrderProcessor(inventory)

        products = [
            Product("P001", "Laptop", Decimal("999.99"), 5),
            Product("P002", "Mouse", Decimal("29.99"), 20),
            Product("P003", "Keyboard", Decimal("79.99"), 15),
        ]

        for product in products:
            inventory.add_product(product)

        return {
            "inventory": inventory,
            "processor": processor,
            "products": products,
        }

    def test_successful_order_processing(self, setup_system):
        """Test complete successful order flow."""
        inventory = setup_system["inventory"]
        processor = setup_system["processor"]
        products = setup_system["products"]

        order = Order(
            order_id="O001",
            items=[
                OrderItem(products[0], 1),
                OrderItem(products[1], 2),
            ],
        )

        success, message = processor.process_order(order)

        assert success is True, "Valid order should be processed successfully"
        assert message == "Order processed successfully", (
            "Successful processing should return the expected message"
        )
        assert inventory.get_product("P001").stock == 4, (
            "Laptop stock should reduce from 5 to 4"
        )
        assert inventory.get_product("P002").stock == 18, (
            "Mouse stock should reduce from 20 to 18"
        )
        assert order in processor.processed_orders, (
            "Processed order should be stored in processed_orders"
        )

    def test_order_validation_failure_out_of_stock(self, setup_system):
        """Test order validation fails for out-of-stock items."""
        processor = setup_system["processor"]
        products = setup_system["products"]

        order = Order(
            order_id="O002",
            items=[
                OrderItem(products[0], 10),
            ],
        )

        is_valid, error_message = processor.validate_order(order)

        assert is_valid is False, "Order should fail validation when stock is insufficient"
        assert "P001" in error_message, (
            "Error message should identify the product causing validation failure"
        )

    def test_order_processing_failure_maintains_inventory(self, setup_system):
        """Test that failed orders do not modify inventory."""
        inventory = setup_system["inventory"]
        processor = setup_system["processor"]
        products = setup_system["products"]

        initial_laptop_stock = inventory.get_product("P001").stock

        order = Order(
            order_id="O003",
            items=[
                OrderItem(products[0], 99),
            ],
        )

        success, message = processor.process_order(order)

        assert success is False, "Out-of-stock order should not be processed"
        assert "P001" in message, "Failure message should identify the unavailable product"
        assert inventory.get_product("P001").stock == initial_laptop_stock, (
            "Inventory should remain unchanged after failed processing"
        )
        assert order not in processor.processed_orders, (
            "Failed order should not be added to processed_orders"
        )

    def test_multiple_orders_sequential_processing(self, setup_system):
        """Test processing multiple orders sequentially."""
        inventory = setup_system["inventory"]
        processor = setup_system["processor"]
        products = setup_system["products"]

        orders = [
            Order("O004", [OrderItem(products[1], 2)]),
            Order("O005", [OrderItem(products[2], 3)]),
            Order("O006", [OrderItem(products[0], 1), OrderItem(products[1], 1)]),
        ]

        for order in orders:
            success, message = processor.process_order(order)
            assert success is True, f"{order.order_id} should process successfully: {message}"

        assert inventory.get_product("P001").stock == 4, (
            "Laptop stock should reflect one unit sold"
        )
        assert inventory.get_product("P002").stock == 17, (
            "Mouse stock should reflect three units sold"
        )
        assert inventory.get_product("P003").stock == 12, (
            "Keyboard stock should reflect three units sold"
        )
        assert len(processor.processed_orders) == 3, (
            "All three successful orders should be tracked"
        )

    def test_order_with_discount_integration(self, setup_system):
        """Test order processing with discount applied."""
        inventory = setup_system["inventory"]
        processor = setup_system["processor"]
        products = setup_system["products"]

        order = Order(
            order_id="O007",
            items=[
                OrderItem(products[0], 1),
                OrderItem(products[1], 1),
            ],
            discount_percent=Decimal("10"),
        )

        success, message = processor.process_order(order)

        assert success is True, f"Discounted order should process successfully: {message}"
        assert order.calculate_total() == Decimal("926.982"), (
            "Total should include 10 percent discount"
        )
        assert inventory.get_product("P001").stock == 4, (
            "Laptop stock should reduce after discounted order"
        )
        assert inventory.get_product("P002").stock == 19, (
            "Mouse stock should reduce after discounted order"
        )
