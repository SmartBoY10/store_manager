from django.shortcuts import render
from django.views.generic.base import View
from .models import *


class ProductsView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, "store_app/index.html", {"product_list":products})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        return render(request, "store_app/product_detail.html", {"product":product})