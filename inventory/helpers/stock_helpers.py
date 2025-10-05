"""
Helper functions for stock adjustment operations.
"""

import logging
from typing import Dict, Any

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from ..models import Product
from ..serializers import StockAdjustmentSerializer
from ..services import InventoryService
from .responses import APIResponse
from .exceptions import InsufficientStockException

logger = logging.getLogger(__name__)


def validate_stock_adjustment_data(data: Dict[str, Any]) -> int:
    """
    Validate stock adjustment request data.

    Args:
        data: Request data containing quantity

    Returns:
        int: Validated quantity

    Raises:
        ValidationError: If data is invalid
    """
    serializer = StockAdjustmentSerializer(data=data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    quantity = serializer.validated_data['quantity']

    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero")

    return quantity


def perform_stock_increase(product_id: int, quantity: int, user_id: int) -> Dict[str, Any]:
    """
    Perform stock increase operation.

    Args:
        product_id: ID of the product
        quantity: Quantity to add
        user_id: ID of the user making the change

    Returns:
        Dict containing product data and adjustment details

    Raises:
        Product.DoesNotExist: If product not found
        ValueError: If invalid data
    """
    product = InventoryService.increase_stock(
        product_id=product_id,
        quantity=quantity,
        user_id=user_id
    )

    logger.info(
        f"Stock increased for product {product.name} (ID: {product_id}) "
        f"by {quantity} units. New stock: {product.stock_quantity}"
    )

    return {
        'product': product,
        'adjustment': {
            'quantity_added': quantity,
            'previous_stock': product.stock_quantity - quantity,
            'current_stock': product.stock_quantity
        }
    }


def perform_stock_decrease(product_id: int, quantity: int, user_id: int) -> Dict[str, Any]:
    """
    Perform stock decrease operation.

    Args:
        product_id: ID of the product
        quantity: Quantity to subtract
        user_id: ID of the user making the change

    Returns:
        Dict containing product data and adjustment details

    Raises:
        Product.DoesNotExist: If product not found
        InsufficientStockException: If insufficient stock
        ValueError: If invalid data
    """
    product = InventoryService.decrease_stock(
        product_id=product_id,
        quantity=quantity,
        user_id=user_id
    )

    logger.info(
        f"Stock decreased for product {product.name} (ID: {product_id}) "
        f"by {quantity} units. New stock: {product.stock_quantity}"
    )

    return {
        'product': product,
        'adjustment': {
            'quantity_removed': quantity,
            'previous_stock': product.stock_quantity + quantity,
            'current_stock': product.stock_quantity
        }
    }


def handle_stock_adjustment_error(error: Exception, operation: str) -> Response:
    """
    Handle errors for stock adjustment operations.

    Args:
        error: The exception that occurred
        operation: Description of the operation (e.g., "increase stock")

    Returns:
        Response: Formatted error response
    """
    if isinstance(error, Product.DoesNotExist):
        return APIResponse.error(
            message="Product not found",
            error_details=f"No product found with the given ID",
            status_code=status.HTTP_404_NOT_FOUND
        )
    elif isinstance(error, InsufficientStockException):
        return APIResponse.error(
            message="Insufficient stock",
            error_details=str(error),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    elif isinstance(error, ValidationError):
        return APIResponse.validation_error(error.messages)
    elif isinstance(error, ValueError):
        return APIResponse.error(
            message="Invalid input data",
            error_details=str(error),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    else:
        logger.error(f"Unexpected error in {operation}: {str(error)}")
        return APIResponse.error(
            message=f"Failed to {operation}",
            error_details="An unexpected error occurred. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
