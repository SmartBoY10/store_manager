from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *

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
            for product in products:
                purchases = Purchase.objects.filter(storage_id=storage.id, product_id=product.id)
                sales = Sale.objects.filter(storage_id=storage.id, product_id=product.id)
                for purchase, sale in zip(purchases, sales):
                    q_purchase = 0
                    q_sale = 0
                    q_purchase += purchase.quantity
                    q_sale += sale.quantity
                    quantity = q_purchase - q_sale
                    return quantity

        context = {"storages": storages, "products": products}
        return render(request, "storage_app/storages.html", context)


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
        else:
            print("Qotaqbass Fikusx")
        return redirect("/")


class SaleView(View):
    def get(self, request):
        sales = Sale.objects.all()
        return render(request, "storage_app/sale.html", {"sales": sales})