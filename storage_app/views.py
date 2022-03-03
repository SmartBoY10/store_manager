from django.shortcuts import render
from django.views import View
from .models import *

class ManualView(View):
    def get(self, request):
        manuals = Manual.objects.all()
        return render(request, "storage_app/index.html", {"manuals": manuals})


class ManualDetailView(View):
    def get(self, request, pk):
        storages = Manual.objects.get(id=pk).storage.all()
        return render(request, "storage_app/manual_detail.html", {"storages": storages})


class StorageView(View):
    def get(self, request):
        storages = Storage.objects.all()
        for storage in storages:
            products = Storage.objects.get(id=storage.id).product.all()
            d = {storage.name: products}
        print(d)
        return render(request, "storage_app/storages.html")


class PurchaseView(View):
    def get(self, request):
        purchases = Purchase.objects.all()
        return render(request, "storage_app/purchase.html", {"purchases": purchases})


class SaleView(View):
    def get(self, request):
        sales = Sale.objects.all()
        return render(request, "storage_app/sale.html", {"sales": sales})