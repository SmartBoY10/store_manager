from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *

admin.site.register(Status)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(PayType)
admin.site.register(Storage)
admin.site.register(Purchase)



class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = '__all__'


# @admin.register(Buyer)
# class BuyerAdmin(admin.ModelAdmin):
#     list_display = ("id", "session_id")
#     list_display_links = ("id", "session_id")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "purchase_price_per_unit", "quantity", "sale_price_per_unit")
    list_display_links = ("id", "name")
    form = ProductAdminForm
    readonly_fields = ("quantity",)

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("full_name", "address", "phone", "pay_type", "status", "created_at", "served_at")
    list_display_links = ("full_name",)
    readonly_fields = ("full_name", "address", "phone", "pay_type", "orders")

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "date_of_purchase")