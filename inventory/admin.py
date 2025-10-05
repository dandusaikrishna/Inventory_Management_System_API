from django.contrib import admin
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'stock_quantity', 'low_stock_threshold', 
        'stock_status', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']

    def stock_status(self, obj):
        if not obj.is_active:
            return format_html(
                '<span style="color: gray;">Inactive</span>'
            )
        if obj.is_low_stock:
            return format_html(
                '<span style="color: red;">Low Stock ({}/{})</span>',
                obj.stock_quantity, obj.low_stock_threshold
            )
        return format_html(
            '<span style="color: green;">OK ({}/{})</span>',
            obj.stock_quantity, obj.low_stock_threshold
        )
    stock_status.short_description = 'Stock Status'