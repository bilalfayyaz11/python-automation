import pytest
from decimal import Decimal

from src.order_system.models import Order, OrderItem, Product


@pytest.mark.unit
class TestProduct:
    """Unit tests for Product model."""

    def test_product_creation(self):
        """Test product instantiation with valid data."""
        product = Product(
            id="P001",
            name="Laptop",
            price=Decimal("999.99"),
            stock=10,
        )

        assert product.id == "P001", "Product ID should match the provided value"
        assert product.name == "Laptop", "Product name should match the provided value"
        assert product.price == Decimal("999.99"), "Product price should be exact"
        assert product.stock == 10, "Product stock should match the provided value"

    def test_product_price_type(self):
        """Test that price is stored as Decimal."""
        product = Product(
            id="P002",
            name="Mouse",
            price=Decimal("29.99"),
            stock=50,
        )

        assert isinstance(product.price, Decimal), "Product price should use Decimal"
        assert product.price == Decimal("29.99"), "Decimal price should remain exact"


@pytest.mark.unit
class TestOrderItem:
    """Unit tests for OrderItem model."""

    @pytest.fixture
    def sample_product(self):
        """Fixture providing a sample product."""
        return Product(
            id="P001",
            name="Test Product",
            price=Decimal("29.99"),
            stock=100,
        )

    def test_order_item_subtotal(self, sample_product):
        """Test subtotal calculation for order item."""
        item = OrderItem(product=sample_product, quantity=3)
        expected_subtotal = Decimal("89.97")

        assert item.get_subtotal() == expected_subtotal, (
            "Subtotal should equal product price multiplied by quantity"
        )

    def test_order_item_subtotal_single_quantity(self, sample_product):
        """Test subtotal with quantity of 1."""
        item = OrderItem(product=sample_product, quantity=1)

        assert item.get_subtotal() == sample_product.price, (
            "Subtotal for quantity 1 should equal the product price"
        )


@pytest.mark.unit
class TestOrder:
    """Unit tests for Order model."""

    @pytest.fixture
    def sample_order_items(self):
        """Fixture providing sample order items."""
        laptop = Product("P001", "Laptop", Decimal("999.99"), 10)
        mouse = Product("P002", "Mouse", Decimal("29.99"), 50)
        keyboard = Product("P003", "Keyboard", Decimal("79.99"), 30)

        return [
            OrderItem(laptop, 1),
            OrderItem(mouse, 2),
            OrderItem(keyboard, 1),
        ]

    def test_order_total_no_discount(self, sample_order_items):
        """Test order total calculation without discount."""
        order = Order(order_id="O001", items=sample_order_items)
        expected_total = Decimal("1139.96")

        assert order.calculate_total() == expected_total, (
            "Order total should equal the sum of all item subtotals"
        )

    def test_order_total_with_discount(self, sample_order_items):
        """Test order total with discount applied."""
        order = Order(
            order_id="O002",
            items=sample_order_items,
            discount_percent=Decimal("10"),
        )
        expected_total = Decimal("1025.964")

        assert order.calculate_total() == expected_total, (
            "Order total should apply the percentage discount correctly"
        )

    def test_order_empty_items(self):
        """Test order with no items."""
        order = Order(order_id="O003", items=[])

        assert order.calculate_total() == Decimal("0"), (
            "Order with no items should return a zero total"
        )
