from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *


class StorageViewS(View):
    def get(self, request):
        storages = Storage.objects.all()
        for storage in storages:
            products = Product.objects.filter(storege_id=storage.id)
        

        context = {"storages": storages, "products": products}
        return render(request, "storage_app/index.html", context)


class PurchaseViewS(View):
    def get(self, request):
        purchases = Purchase.objects.all()
        storages = Storage.objects.all()
        for storage in storages:
            products = Product.objects.filter(storege_id=storage.id)
        context = {"purchases": purchases, "storages": storages, "products": products}
        return render(request, "storage_app/purchase.html", context)


class PurchaseProductS(View):
    def post(self, request):
        form = PurchaseForm(request.POST)
        if form.is_valid():
            storage = Storage.objects.get(name=form.cleaned_data['storage'])
            product = Product.objects.get(name=form.cleaned_data['product'])
            quantity = form.cleaned_data['quantity']
            price_per_unit = product.price_per_unit

            Purchase.objects.create(
                storage=storage,
                product=product,
                quantity=quantity,
                price_per_unit=price_per_unit
            )
            product.total_cost += (quantity * price_per_unit)
            product.quantity += quantity
            product.save()
        else:
            print("Qotagbasss")
        return redirect("/storage")


class SaleViewS(View):
    def get(self, request):
        sales = Sale.objects.all()
        storages = Storage.objects.all()
        for storage in storages:
            products = Product.objects.filter(storege_id=storage.id)
        return render(request, "storage_app/sale.html", {"sales": sales, "storages": storages, "products": products})


class SaleProductS(View):
    def post(self, request):
        form = SaleForm(request.POST)
        if form.is_valid():
            storage = Storage.objects.get(name=form.cleaned_data['storage'])
            product = Product.objects.get(name=form.cleaned_data['product'])
            quantity = form.cleaned_data['quantity']
            purchase_price_per_unit = product.price_per_unit
            sale_price_per_unit = form.cleaned_data['sale_price_per_unit']
            Sale.objects.create(
                storage=storage,
                product=product,
                quantity=quantity,
                purchase_price_per_unit=purchase_price_per_unit,
                sale_price_per_unit=sale_price_per_unit
            )
            product.total_cost -= (quantity * purchase_price_per_unit)
            product.quantity -= form.cleaned_data['quantity']
            product.save()
        return redirect("/storage")