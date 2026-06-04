import pytest
from decimal import Decimal

from src.order_system.inventory import InventoryManager
from src.order_system.models import Product


@pytest.mark.unit
class TestInventoryManager:
    """Unit tests for InventoryManager."""

    @pytest.fixture
    def inventory(self):
        """Fixture providing fresh InventoryManager instance."""
        return InventoryManager()

    @pytest.fixture
    def sample_product(self):
        """Fixture providing a sample product."""
        return Product(
            id="P001",
            name="Laptop",
            price=Decimal("999.99"),
            stock=10,
        )

    def test_add_product(self, inventory, sample_product):
        """Test adding product to inventory."""
        inventory.add_product(sample_product)

        assert "P001" in inventory.products, "Product ID should exist in inventory"
        assert inventory.products["P001"] == sample_product, (
            "Stored product should match the original product"
        )

    def test_get_product_exists(self, inventory, sample_product):
        """Test retrieving existing product."""
        inventory.add_product(sample_product)

        retrieved_product = inventory.get_product("P001")

        assert retrieved_product == sample_product, (
            "Retrieved product should match the product added to inventory"
        )

    def test_get_product_not_exists(self, inventory):
        """Test retrieving non-existent product."""
        retrieved_product = inventory.get_product("UNKNOWN")

        assert retrieved_product is None, "Unknown product IDs should return None"

    def test_check_availability_sufficient_stock(self, inventory, sample_product):
        """Test availability check with sufficient stock."""
        inventory.add_product(sample_product)

        is_available = inventory.check_availability("P001", 5)

        assert is_available is True, "Quantity 5 should be available from stock 10"

    def test_check_availability_insufficient_stock(self, inventory, sample_product):
        """Test availability check with insufficient stock."""
        inventory.add_product(sample_product)

        is_available = inventory.check_availability("P001", 15)

        assert is_available is False, "Quantity 15 should not be available from stock 10"

    def test_reduce_stock_success(self, inventory, sample_product):
        """Test successful stock reduction."""
        inventory.add_product(sample_product)

        result = inventory.reduce_stock("P001", 3)

        assert result is True, "Stock reduction should succeed when stock is available"
        assert inventory.get_product("P001").stock == 7, (
            "Stock should be reduced from 10 to 7"
        )

    def test_reduce_stock_failure(self, inventory, sample_product):
        """Test stock reduction failure with insufficient stock."""
        inventory.add_product(sample_product)

        result = inventory.reduce_stock("P001", 15)

        assert result is False, "Stock reduction should fail when stock is insufficient"
        assert inventory.get_product("P001").stock == 10, (
            "Stock should remain unchanged after failed reduction"
        )
