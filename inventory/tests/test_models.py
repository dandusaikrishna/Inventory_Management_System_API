import pytest
from django.core.exceptions import ValidationError
from apps.inventory.models import Product


@pytest.mark.django_db
class TestProductModel:
    def test_product_creation_valid(self):
        """Test creating a product with valid data."""
        product = Product.objects.create(
            name="Valid Product",
            description="A valid product",
            stock_quantity=10,
            low_stock_threshold=5
        )
        assert product.name == "Valid Product"
        assert product.stock_quantity == 10
        assert product.low_stock_threshold == 5
        assert product.is_active is True

    def test_product_name_unique(self):
        """Test that product names must be unique."""
        Product.objects.create(name="Unique Product", stock_quantity=0)
        with pytest.raises(Exception):  # IntegrityError from database
            Product.objects.create(name="Unique Product", stock_quantity=0)

    def test_clean_negative_stock_quantity(self):
        """Test that clean() raises ValidationError for negative stock_quantity."""
        product = Product(
            name="Test Product",
            stock_quantity=-1,
            low_stock_threshold=5
        )
        with pytest.raises(ValidationError, match="Stock quantity cannot be negative"):
            product.clean()

    def test_clean_negative_low_stock_threshold(self):
        """Test that clean() raises ValidationError for negative low_stock_threshold."""
        product = Product(
            name="Test Product",
            stock_quantity=10,
            low_stock_threshold=-1
        )
        with pytest.raises(ValidationError, match="Low stock threshold cannot be negative"):
            product.clean()

    def test_is_low_stock_property_true(self):
        """Test is_low_stock property returns True when stock <= threshold."""
        product = Product(
            name="Low Stock Product",
            stock_quantity=5,
            low_stock_threshold=10
        )
        assert product.is_low_stock is True

    def test_is_low_stock_property_false(self):
        """Test is_low_stock property returns False when stock > threshold."""
        product = Product(
            name="Normal Stock Product",
            stock_quantity=15,
            low_stock_threshold=10
        )
        assert product.is_low_stock is False

    def test_can_reduce_stock_sufficient(self):
        """Test can_reduce_stock returns True when enough stock is available."""
        product = Product(
            name="Test Product",
            stock_quantity=10,
            low_stock_threshold=5
        )
        assert product.can_reduce_stock(5) is True
        assert product.can_reduce_stock(10) is True

    def test_can_reduce_stock_insufficient(self):
        """Test can_reduce_stock returns False when not enough stock."""
        product = Product(
            name="Test Product",
            stock_quantity=5,
            low_stock_threshold=10
        )
        assert product.can_reduce_stock(10) is False
        assert product.can_reduce_stock(6) is False

    def test_can_reduce_stock_exact(self):
        """Test can_reduce_stock returns True for exact stock match."""
        product = Product(
            name="Test Product",
            stock_quantity=5,
            low_stock_threshold=10
        )
        assert product.can_reduce_stock(5) is True

    def test_str_method(self):
        """Test the __str__ method returns correct format."""
        product = Product(
            name="Test Product",
            stock_quantity=15
        )
        assert str(product) == "Test Product (Stock: 15)"
