from django.db import transaction
from .models import Product
from .helpers.exceptions import InsufficientStockException

class InventoryService:
    """Service class for inventory operations."""
    
    @staticmethod
    @transaction.atomic
    def increase_stock(product_id: int, quantity: int) -> Product:
        """
        Increase stock quantity for a product.
        
        Args:
            product_id: ID of the product
            quantity: Quantity to add (must be positive)
            
        Returns:
            Updated Product instance
        """
        product = Product.objects.get(id=product_id)
        product.stock_quantity += quantity
        product.save()
        return product
    
    @staticmethod
    @transaction.atomic
    def decrease_stock(product_id: int, quantity: int) -> Product:
        """
        Decrease stock quantity for a product.
        
        Args:
            product_id: ID of the product
            quantity: Quantity to remove (must be positive)
            
        Returns:
            Updated Product instance
            
        Raises:
            InsufficientStockException: If not enough stock available
        """
        product = Product.objects.get(id=product_id)
        
        if not product.can_reduce_stock(quantity):
            raise InsufficientStockException(
                f"Insufficient stock. Available: {product.stock_quantity}, "
                f"Requested: {quantity}"
            )
        
        product.stock_quantity -= quantity
        product.save()
        return product
    
    @staticmethod
    def get_low_stock_products():
        """Get all products that are below their low stock threshold."""
        from django.db.models import F
        
        return Product.objects.filter(
            is_active=True,
            stock_quantity__lte=F('low_stock_threshold')
        ).order_by('stock_quantity')

    @staticmethod
    def get_stock_history(product_id: int):
        """Get stock adjustment history for a product. (Stub implementation)"""
        # Placeholder for stock history logic
        return []
    
    @staticmethod
    def get_inventory_summary():
        """Get overall inventory summary statistics. (Stub implementation)"""
        from django.db.models import F
        
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(
            stock_quantity__lte=F('low_stock_threshold')
        ).count()
        out_of_stock_count = Product.objects.filter(stock_quantity=0).count()
        
        return {
            'total_products': total_products,
            'low_stock_products': low_stock_count,
            'out_of_stock_products': out_of_stock_count
        }
