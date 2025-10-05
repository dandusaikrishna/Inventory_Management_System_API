from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'stock_quantity',
            'low_stock_threshold', 'is_active', 'is_low_stock',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class StockAdjustmentSerializer(serializers.Serializer):
    """Serializer for stock adjustment operations."""
    
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be positive")
        return value