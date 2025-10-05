from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Product CRUD endpoints
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Stock management endpoints
    path('products/<int:product_id>/increase-stock/', views.increase_stock, name='increase-stock'),
    path('products/<int:product_id>/decrease-stock/', views.decrease_stock, name='decrease-stock'),
    
    # Low stock endpoint
    path('products/low-stock/', views.low_stock_products, name='low-stock-products'),
]