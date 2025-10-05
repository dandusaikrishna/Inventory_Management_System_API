"""
Helper module for standardized API responses and pagination.
"""

import logging
from typing import Dict, Any

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Configure logging
logger = logging.getLogger(__name__)


class APIResponse:
    """Standardized API response formatter"""

    @staticmethod
    def success(data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK) -> Response:
        """Format successful response"""
        response_data = {
            "success": True,
            "message": message,
            "data": data,
            "error": None
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message: str, error_details: Any = None, status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
        """Format error response"""
        response_data = {
            "success": False,
            "message": message,
            "data": None,
            "error": error_details
        }
        logger.error(f"API Error: {message} - Details: {error_details}")
        return Response(response_data, status=status_code)

    @staticmethod
    def validation_error(serializer_errors: Dict) -> Response:
        """Format validation error response"""
        return APIResponse.error(
            message="Validation failed",
            error_details=serializer_errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class with company standards"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """Override to match company response format"""
        return APIResponse.success(
            data={
                'results': data,
                'pagination': {
                    'count': self.page.paginator.count,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'page_size': self.get_page_size(self.request),
                    'total_pages': self.page.paginator.num_pages,
                    'current_page': self.page.number
                }
            },
            message="Data retrieved successfully"
        )
