from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('products/', ProductsView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/category/<int:pk>/', ProductsByCategoryView.as_view(), name='by_category'),
    path('about/', AboutView.as_view(), name='about'),
    path('faqs/', FaqsView.as_view(), name='faqs'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('product/add-to-cart/<int:pk>/', AddToCart.as_view(), name='add_to_cart'),
    path('product/add_to_cart_with_quantity/', AddToCartWithQuantity.as_view(), name='add_to_cart_with_quantity'),
    path('product/add_new_cart_with_quantity/<int:pk>', AddNewCartWithQuantity.as_view(), name='add_new_cart_with_quantity'),
    path('cart-detail/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/delete/<int:pk>/', DeleteFromCart.as_view(), name='delete_from_cart'),
    path('cart/confirm-delete/<int:pk>/', ConfirmDelete.as_view(), name='confirm_delete'),
    path('take-order/<int:pk>/', TakeOrder.as_view(), name='take-order'),
    path('confirm/<int:pk>/', Confirm.as_view(), name='confirm'),
    path('storage/', StorageView.as_view(), name='storage'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('sale/', SaleView.as_view(), name='sale'),
    path('storages/', StorageView.as_view(), name='storages'),
    path('purchase-product/', PurchaseProduct.as_view(), name='purchase_product'),
    path('sale-product/', SaleProduct.as_view(), name='sale_product'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
]
