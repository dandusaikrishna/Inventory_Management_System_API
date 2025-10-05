from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class TimeStampedModel(models.Model):
    """Abstract base class for models with created and updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(TimeStampedModel):
    """Product model representing inventory items."""
    
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Product name must be unique"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed product description"
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Current stock quantity (cannot be negative)"
    )
    low_stock_threshold = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        help_text="Threshold below which product is considered low stock"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the product is active in inventory"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Stock: {self.stock_quantity})"

    def clean(self):
        """Custom validation for the model."""
        if self.stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative")
        
        if self.low_stock_threshold < 0:
            raise ValidationError("Low stock threshold cannot be negative")

    @property
    def is_low_stock(self):
        """Check if product is below low stock threshold."""
        return self.stock_quantity <= self.low_stock_threshold

    def can_reduce_stock(self, quantity):
        """Check if stock can be reduced by given quantity."""
        return self.stock_quantity >= quantity