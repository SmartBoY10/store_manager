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

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ("id", "session_id", "full_name", "address", "phone", "city", "pay_type")
    list_display_links = ("id", "full_name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_name")
    list_display_links = ("id", "name")

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("full_name", "address", "phone", "pay_type", "status", "created_at", "served_at")
    list_display_links = ("full_name",)
    readonly_fields = ("full_name", "address", "phone", "pay_type", "orders")