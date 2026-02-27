from django.contrib import admin
from .models import Customer, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "language", "current_step", "is_active", "created_at")
    search_fields = ("phone_number",)
    list_filter = ("language", "current_step", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)