from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

class InventoryException(Exception):
    """Base exception for inventory-related errors."""
    pass

class InsufficientStockException(InventoryException):
    """Raised when trying to reduce stock below available quantity."""
    pass

def custom_exception_handler(exc, context):
    """Custom exception handler for inventory exceptions."""
    response = exception_handler(exc, context)

    if isinstance(exc, InsufficientStockException):
        return Response({
            'error': 'Insufficient stock available',
            'detail': str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)

    return response