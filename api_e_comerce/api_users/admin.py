from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from .models import User


@admin.register(User)
class UserAdmin(UA):
    # fieldsets = (
    #     ('Dirección', {'fields': ('address',)}),
    # )
    pass
