from django.urls import path
from .views import *

urlpatterns = [
    path('', ManualView.as_view(), name='storage_home'),
    path('manual/<int:pk>/', ManualDetailView.as_view(), name='manual_detail'),
    path('manual/purchase/', PurchaseView.as_view(), name='purchase'),
    path('manual/sale/', SaleView.as_view(), name='sale'),
    path('manual/storages/', StorageView.as_view(), name='storages'),
    path('manual/purchase-product/', PurchaseProduct.as_view(), name='purchase_product')
]