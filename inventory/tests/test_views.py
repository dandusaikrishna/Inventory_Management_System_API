import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.inventory.models import Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def product():
    return Product.objects.create(
        name="Test Product",
        description="Test Description",
        stock_quantity=10,
        low_stock_threshold=5
    )

@pytest.mark.django_db
class TestProductAPI:
    def test_create_product(self, api_client):
        url = reverse('inventory:product-list-create')
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'stock_quantity': 20,
            'low_stock_threshold': 5
        }
        
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == data['name']
        assert response.data['stock_quantity'] == data['stock_quantity']

    def test_increase_stock(self, api_client, product):
        url = reverse('inventory:increase-stock', args=[product.id])
        initial_quantity = product.stock_quantity
        increase_by = 5
        
        response = api_client.post(url, {'quantity': increase_by})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['product']['stock_quantity'] == initial_quantity + increase_by

    def test_decrease_stock_success(self, api_client, product):
        url = reverse('inventory:decrease-stock', args=[product.id])
        initial_quantity = product.stock_quantity
        decrease_by = 5
        
        response = api_client.post(url, {'quantity': decrease_by})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['product']['stock_quantity'] == initial_quantity - decrease_by

    def test_decrease_stock_insufficient(self, api_client, product):
        url = reverse('inventory:decrease-stock', args=[product.id])
        decrease_by = product.stock_quantity + 1
        
        response = api_client.post(url, {'quantity': decrease_by})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_low_stock_products(self, api_client, product):
        # Set stock below threshold
        product.stock_quantity = product.low_stock_threshold - 1
        product.save()
        
        url = reverse('inventory:low-stock-products')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert any(p['id'] == product.id for p in response.data)