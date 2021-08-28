from django.contrib import admin
from .models import Stock, StockDetail


# Register your models here.

admin.site.register(Stock)
admin.site.register(StockDetail)