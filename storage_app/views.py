from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *


class StorageView(View):
    def get(self, request):
        storages = Storage.objects.all()
        for storage in storages:
            products = Storage.objects.get(id=storage.id).product.all()
        

        context = {"storages": storages, "products": products}
        return render(request, "storage_app/index.html", context)


class PurchaseView(View):
    def get(self, request):
        purchases = Purchase.objects.all()
        storages = Storage.objects.all()
        products = Product.objects.all()
        context = {"purchases": purchases, "storages": storages, "products": products}
        return render(request, "storage_app/purchase.html", context)


class PurchaseProduct(View):
    def post(self, request):
        form = PurchaseForm(request.POST)
        if form.is_valid():
            storage = Storage.objects.get(name=form.cleaned_data['storage'])
            product = Product.objects.get(name=form.cleaned_data['product'])
            Purchase.objects.create(
                storage=storage,
                product=product,
                quantity=form.cleaned_data['quantity'],
                price_per_unit=form.cleaned_data['price_per_unit']
            )
            product.quantity += form.cleaned_data['quantity']
            product.save()
        return redirect("/storage")


class SaleView(View):
    def get(self, request):
        sales = Sale.objects.all()
        storages = Storage.objects.all()
        products = Product.objects.all()
        return render(request, "storage_app/sale.html", {"sales": sales, "storages": storages, "products": products})


class SaleProduct(View):
    def post(self, request):
        form = SaleForm(request.POST)
        if form.is_valid():
            storage = Storage.objects.get(name=form.cleaned_data['storage'])
            product = Product.objects.get(name=form.cleaned_data['product'])
            Sale.objects.create(
                storage=storage,
                product=product,
                quantity=form.cleaned_data['quantity'],
                price_per_unit=form.cleaned_data['price_per_unit']
            )
            product.quantity -= form.cleaned_data['quantity']
            product.save()
        return redirect("/storage")