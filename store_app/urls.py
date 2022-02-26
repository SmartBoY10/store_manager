from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductsView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail')
]
