from django.urls import path
from .views import *

urlpatterns = [
    path('', StorageView.as_view(), name='storage_home'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('sale/', SaleView.as_view(), name='sale'),
    path('storages/', StorageView.as_view(), name='storages'),
    path('purchase-product/', PurchaseProduct.as_view(), name='purchase_product'),
    path('sale-product/', SaleProduct.as_view(), name='sale_product'),
]