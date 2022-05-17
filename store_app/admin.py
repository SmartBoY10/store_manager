from django.contrib import admin
from .models import *

admin.site.register(Status)
admin.site.register(Brand)
admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Buyer)
admin.site.register(Cart)
admin.site.register(Order)
# admin.site.register(Journal)
admin.site.register(PayType)
admin.site.register(Storage)
admin.site.register(Purchase)
admin.site.register(Sale)

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ("id", "session_id")
    list_display_links = ("id", "session_id")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "purchase_price_per_unit", "quantity", "sale_price_per_unit")
    list_display_links = ("id", "name")
    readonly_fields = ("quantity",)

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("full_name", "address", "phone", "pay_type", "status", "created_at", "served_at")
    list_display_links = ("full_name",)
    readonly_fields = ("full_name", "address", "phone", "pay_type", "orders")