from django.core.exceptions import ValidationError
from rest_framework import serializers

def validate_positive_integer(value):
    """Validate that value is a positive integer."""
    if not isinstance(value, int) or value <= 0:
        raise serializers.ValidationError("Value must be a positive integer")
    return value

def validate_non_negative_integer(value):
    """Validate that value is a non-negative integer."""
    if not isinstance(value, int) or value < 0:
        raise serializers.ValidationError("Value must be a non-negative integer")
    return value

def validate_product_name(value):
    """Validate product name."""
    if len(value.strip()) < 2:
        raise serializers.ValidationError("Product name must be at least 2 characters long")
    return value.strip()