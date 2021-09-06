from django.contrib import admin
from .models import Product, Supplier, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'category', 'unit_price', 'supplier', 'stock_unit', 'active']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Supplier)

