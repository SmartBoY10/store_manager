from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductsView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('product/add-to-cart/<int:pk>/', AddToCart.as_view(), name='add_to_cart'),
    path('product/add_to_cart_with_quantity/', AddToCartWithQuantity.as_view(), name='add_to_cart_with_quantity'),
    path('cart-detail/', CartDetailView.as_view(), name='cart_detail'),
]
