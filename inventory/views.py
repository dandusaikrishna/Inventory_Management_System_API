"""
Product Inventory Management API Views
Simple CRUD and inventory management endpoints
"""

from django.db.models import F

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    """
    Handle product list and create operations
    GET:  /api/products/ - List all products
    POST: /api/products/ - Create new product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handle single product operations
    GET:    /api/products/{id}/ - Get product details
    PUT:    /api/products/{id}/ - Update product
    DELETE: /api/products/{id}/ - Delete product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['POST'])
def increase_stock(request, product_id):
    """
    Increase product stock quantity
    Expected JSON body: {"quantity": number}
    """
    try:
        product = Product.objects.get(id=product_id)
        quantity = request.data.get('quantity')
        
        if not quantity or quantity <= 0:
            return Response(
                {'error': 'Quantity must be a positive number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.stock_quantity += quantity
        product.save()
        
        return Response({
            'success': True,
            'message': f'Stock increased by {quantity} units',
            'data': ProductSerializer(product).data
        })
        
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception:
        return Response(
            {'error': 'Failed to increase stock'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def decrease_stock(request, product_id):
    """
    Decrease product stock quantity
    Expected JSON body: {"quantity": number}
    """
    try:
        product = Product.objects.get(id=product_id)
        quantity = request.data.get('quantity')
        
        if not quantity or quantity <= 0:
            return Response(
                {'error': 'Quantity must be a positive number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if product.stock_quantity < quantity:
            return Response(
                {'error': 'Insufficient stock available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product.stock_quantity -= quantity
        product.save()
        
        return Response({
            'success': True,
            'message': f'Stock decreased by {quantity} units',
            'data': ProductSerializer(product).data
        })
        
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception:
        return Response(
            {'error': 'Failed to decrease stock'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def low_stock_products(request):
    """
    Get all products with low stock
    Returns products where stock_quantity <= low_stock_threshold
    """
    try:
        products = Product.objects.filter(
            stock_quantity__lte=F('low_stock_threshold')
        ).order_by('stock_quantity')
        
        serializer = ProductSerializer(products, many=True)
        return Response({
            'success': True,
            'message': f'Found {len(serializer.data)} low stock products',
            'data': serializer.data
        })
        
    except Exception:
        return Response(
            {'error': 'Failed to retrieve low stock products'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )