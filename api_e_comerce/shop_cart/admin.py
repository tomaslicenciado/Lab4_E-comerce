from django.contrib import admin
from .models import ShopState, ShopDetailState, ShopCart


admin.site.register(ShopState)
admin.site.register(ShopDetailState)
admin.site.register(ShopCart)