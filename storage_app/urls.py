from django.urls import path
from .views import *

urlpatterns = [
    path('', StorageViewS.as_view(), name='storage_home'),
    path('purchaseS/', PurchaseViewS.as_view(), name='purchase'),
    path('saleS/', SaleViewS.as_view(), name='sale'),
    path('storagesS/', StorageViewS.as_view(), name='storages'),
    path('purchase-productS/', PurchaseProductS.as_view(), name='purchase_product'),
    path('sale-productS/', SaleProductS.as_view(), name='sale_product'),
]