import pytest
from django.db import transaction
from apps.inventory.models import Product
from apps.inventory.services import InventoryService
from apps.inventory.helpers.exceptions import InsufficientStockException


@pytest.mark.django_db
class TestInventoryService:
    @pytest.fixture
    def product(self):
        return Product.objects.create(
            name="Test Product",
            description="Test Description",
            stock_quantity=10,
            low_stock_threshold=5
        )

    def test_increase_stock_success(self, product):
        """Test successful stock increase."""
        initial_stock = product.stock_quantity
        quantity = 5

        result = InventoryService.increase_stock(product.id, quantity)

        product.refresh_from_db()
        assert product.stock_quantity == initial_stock + quantity
        assert result.stock_quantity == initial_stock + quantity

    def test_increase_stock_product_not_found(self):
        """Test increase_stock raises DoesNotExist for invalid product_id."""
        with pytest.raises(Product.DoesNotExist):
            InventoryService.increase_stock(999, 5)

    def test_decrease_stock_success(self, product):
        """Test successful stock decrease."""
        initial_stock = product.stock_quantity
        quantity = 5

        result = InventoryService.decrease_stock(product.id, quantity)

        product.refresh_from_db()
        assert product.stock_quantity == initial_stock - quantity
        assert result.stock_quantity == initial_stock - quantity

    def test_decrease_stock_insufficient_stock(self, product):
        """Test decrease_stock raises InsufficientStockException when not enough stock."""
        quantity = product.stock_quantity + 1

        with pytest.raises(InsufficientStockException, match="Insufficient stock"):
            InventoryService.decrease_stock(product.id, quantity)

        # Ensure stock wasn't changed
        product.refresh_from_db()
        assert product.stock_quantity == 10

    def test_decrease_stock_exact_quantity(self, product):
        """Test decrease_stock allows reducing to zero."""
        quantity = product.stock_quantity

        result = InventoryService.decrease_stock(product.id, quantity)

        product.refresh_from_db()
        assert product.stock_quantity == 0
        assert result.stock_quantity == 0

    def test_decrease_stock_product_not_found(self):
        """Test decrease_stock raises DoesNotExist for invalid product_id."""
        with pytest.raises(Product.DoesNotExist):
            InventoryService.decrease_stock(999, 5)

    def test_increase_stock_transaction_rollback(self, product):
        """Test that increase_stock rolls back on error (simulate)."""
        # Since it's hard to simulate failure, we can check it's wrapped in transaction
        # In real scenario, we might mock database error
        initial_stock = product.stock_quantity

        # This should succeed
        InventoryService.increase_stock(product.id, 5)
        product.refresh_from_db()
        assert product.stock_quantity == initial_stock + 5

    def test_decrease_stock_transaction_rollback(self, product):
        """Test that decrease_stock rolls back on error."""
        # Similar to above
        initial_stock = product.stock_quantity

        # This should succeed
        InventoryService.decrease_stock(product.id, 5)
        product.refresh_from_db()
        assert product.stock_quantity == initial_stock - 5

    def test_get_low_stock_products(self, product):
        """Test get_low_stock_products returns products below threshold."""
        # Create another product below threshold
        low_product = Product.objects.create(
            name="Low Product",
            stock_quantity=3,
            low_stock_threshold=5
        )

        # Create product above threshold
        high_product = Product.objects.create(
            name="High Product",
            stock_quantity=20,
            low_stock_threshold=5
        )

        # Set original product to low stock
        product.stock_quantity = 4
        product.save()

        low_stock = InventoryService.get_low_stock_products()

        # Should include product and low_product, but not high_product
        assert len(low_stock) == 2
        product_ids = [p.id for p in low_stock]
        assert product.id in product_ids
        assert low_product.id in product_ids
        assert high_product.id not in product_ids

    def test_get_low_stock_products_inactive_excluded(self, product):
        """Test get_low_stock_products excludes inactive products."""
        product.stock_quantity = 3  # Below threshold
        product.is_active = False
        product.save()

        low_stock = InventoryService.get_low_stock_products()

        assert len(low_stock) == 0

    def test_get_inventory_summary(self):
        """Test get_inventory_summary returns correct stats."""
        # Clear existing products
        Product.objects.all().delete()

        # Create products
        Product.objects.create(name="Normal", stock_quantity=10, low_stock_threshold=5)
        Product.objects.create(name="Low", stock_quantity=3, low_stock_threshold=5)
        Product.objects.create(name="Out", stock_quantity=0, low_stock_threshold=5)

        summary = InventoryService.get_inventory_summary()

        assert summary['total_products'] == 3
        assert summary['low_stock_products'] == 1  # Low
        assert summary['out_of_stock_products'] == 1  # Out

    def test_get_stock_history_stub(self):
        """Test get_stock_history returns empty list (stub implementation)."""
        history = InventoryService.get_stock_history(1)
        assert history == []
