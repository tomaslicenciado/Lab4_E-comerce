from django.contrib import admin
from .models import PayMethod, Sale

admin.site.register(PayMethod)
admin.site.register(Sale)