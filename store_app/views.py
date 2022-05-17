from itertools import product
from math import prod
from multiprocessing import context
from django.shortcuts import redirect, render
from django.views.generic.base import View

from .models import *
from .forms import *


class AboutView(View):
    def get(self, request):
        return render(request, "store_app/about.html")


class IndexView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.filter(parent=True)
        context = {"product_list":products, "category_list": categories}
        return render(request, "store_app/index.html", context)


class ProductsView(View):
    def get(self, request):
        products_slider = Product.objects.all()
        # categories = Category.objects.filter(parent=True)
        categories = Category.objects.filter(parent=True)
        # product_list = {}
        # list = []
        # for category in categories:
        #     products = Product.objects.filter(category_id=category.id)
            # list.append(products)
            # product_list[category.name] = list
        print(categories)
        context = {"category_list": categories,
                    "products_slider": products_slider}
        return render(request, "store_app/products.html", context)


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        return render(request, "store_app/product_detail.html", {"product":product})


class ProductsByCategoryView(View):
    def get(self, request, pk):
        products = Product.objects.filter(category_id=pk)
        context = {"products": products}
        return render(request, "store_app/products_by_category.html", context)


class FaqsView(View):
    def get(self, request):
        return render(request, "store_app/faqs.html")


class ContactView(View):
    def get(self, request):
        return render(request, "store_app/contact.html")


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        product.view_count += 1
        product.save()
        categories = Category.objects.filter(parent=True)
        context = {"product":product, "categories": categories}
        return render(request, "store_app/product_detail.html", context)


class AddToCart(View):
    def get(self, request, pk):
        s = request.session
        product = Product.objects.get(id=pk)
        try:
            buyer = Buyer.objects.get(session_id=s.session_key)
            cart = Cart.objects.get(buyer_id=buyer.id)
            try:
                order = Order.objects.get(product_id=product.id, buyer_id=buyer.id)
                order.quantity += 1
                order.total_price += product.get_sale_price()
                order.save()
            except:
                order = Order.objects.create(buyer=buyer, product=product, quantity=1, total_price=product.get_sale_price(), cart=cart)

        except:
            buyer = Buyer.objects.create(session_id=s.session_key)
            cart = Cart.objects.create(buyer=buyer)
            order = Order.objects.create(buyer=buyer, product=product, quantity=1, total_price=product.get_sale_price(), cart=cart)

        return redirect("/cart-detail")


class CartDetailView(View):
    def get(self, request):
        cart_total_price = 0
        s = request.session
        try:
            buyer = Buyer.objects.get(session_id=s.session_key)
            orders = Order.objects.filter(buyer_id=buyer.id)
        except:
            buyer = Buyer.objects.create(session_id=s.session_key)
            Cart.objects.create(buyer=buyer)
            orders = Order.objects.filter(buyer_id=buyer.id)

        for order in orders:
            cart_total_price += order.total_price

        context = {'orders': orders, 'buyer_id': buyer.id, 'cart_total_price': cart_total_price}
        return render(request, "store_app/cart_detail.html", context)


class AddToCartWithQuantity(View):
    def post(self, request):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart_id = form.cleaned_data['cart_id']
            quantity = form.cleaned_data['quantity']
            order = Order.objects.get(id=cart_id)
            order.quantity = quantity
            order.total_price = order.product.get_sale_price() * quantity
            order.save()

        return redirect("/cart-detail")


class AddNewCartWithQuantity(View):
    def post(self, request, pk):
        s = request.session
        product = Product.objects.get(id=pk)
        form = AddNewCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            try:
                buyer = Buyer.objects.get(session_id=s.session_key)
                cart = Cart.objects.get(buyer_id=buyer.id)
                try:
                    order = Order.objects.get(product_id=product.id, buyer_id=buyer.id)
                    order.quantity += quantity
                    order.total_price +=product.get_sale_price() * quantity
                    order.save()
                except:
                    order = Order.objects.create(buyer=buyer, 
                                                product=product, 
                                                quantity=quantity, 
                                                total_price=product.get_sale_price() * quantity, 
                                                cart=cart)
            except:
                buyer = Buyer.objects.create(session_id=s.session_key)
                cart = Cart.objects.create(buyer=buyer)
                order = Order.objects.create(buyer=buyer, 
                                            product=product, 
                                            quantity=quantity, 
                                            total_price=product.get_sale_price() * quantity, 
                                            cart=cart)

        return redirect("/cart-detail")


class DeleteFromCart(View):
    def get(self, request, pk):
        return render(request, "store_app/delete_from_cart.html", {"cart_id":pk})


class ConfirmDelete(View):
    def post(self, request, pk):
        Order.objects.get(id=pk).delete()
        return redirect("/cart-detail")


class TakeOrder(View):
    def get(self, request, pk):
        pay_type = PayType.objects.all()
        return render(request, "store_app/checkout.html", {"buyer_id": pk, "pay_type": pay_type})


class Confirm(View):
    def post(self, request, pk):
        form = ConfirOrderForm(request.POST)
        if form.is_valid():
            buyer = Buyer.objects.get(id=pk)
            orders = Order.objects.filter(buyer_id=pk)
            status = Status.objects.get(status_type='NOT SERVED')
            pay_type = PayType.objects.get(pay_type=form.cleaned_data['pay_type'])

            orders_dict = {}
            for order in orders:
                orders_dict[order.id] = {
                                        "Product": order.product.name, 
                                        "Quantity": order.quantity, 
                                        "Total price": order.total_price
                                        }

                product = Product.objects.get(id=order.product.id)

                Sale.objects.create(
                    product=product,
                    quantity=order.quantity,
                    purchase_price_per_unit=product.purchase_price_per_unit,
                    sale_price_per_unit=product.sale_price_per_unit
                )
                # product.total_cost -= (order.quantity * purchase_price_per_unit)
                product.quantity -= order.quantity
                product.save()

            Journal.objects.create(
                full_name=form.cleaned_data['full_name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
                pay_type=pay_type,
                orders=orders_dict,
                status=status
                )
            Cart.objects.get(buyer_id=pk).delete()
            buyer.delete()
        return redirect("/")
            
            
class StorageView(View):
    def get(self, request):
        storages = Storage.objects.all()
        for storage in storages:
            products = Product.objects.filter(storege_id=storage.id)
        

        context = {"storages": storages, "products": products}
        return render(request, "store_app/storages.html", context)


class PurchaseView(View):
    def get(self, request):
        purchases = Purchase.objects.all()
        storages = Storage.objects.all()
        for storage in storages:
            products = Product.objects.filter(storege_id=storage.id)
        context = {"purchases": purchases, "storages": storages, "products": products}
        return render(request, "storage_app/purchase.html", context)


class PurchaseProduct(View):
    def post(self, request):
        form = PurchaseForm(request.POST)
        if form.is_valid():
            storage = Storage.objects.get(name=form.cleaned_data['storage'])
            product = Product.objects.get(name=form.cleaned_data['product'])
            quantity = form.cleaned_data['quantity']
            price_per_unit = product.purchase_price_per_unit

            Purchase.objects.create(
                storage=storage,
                product=product,
                quantity=quantity,
                price_per_unit=price_per_unit
            )
            # product.total_cost += (quantity * price_per_unit)
            product.quantity += quantity
            product.save()
        else:
            print("Qotagbasss")
        return redirect("/storage")


class SaleView(View):
    def get(self, request):
        sales = Sale.objects.all()
        storages = Storage.objects.all()
        for storage in storages:
            products = Product.objects.filter(storege_id=storage.id)
        return render(request, "store_app/sale.html", {"sales": sales, "storages": storages, "products": products})


class SaleProduct(View):
    def post(self, request):
        form = SaleForm(request.POST)
        if form.is_valid():
            storage = Storage.objects.get(name=form.cleaned_data['storage'])
            product = Product.objects.get(name=form.cleaned_data['product'])
            quantity = form.cleaned_data['quantity']
            purchase_price_per_unit = product.price
            sale_price_per_unit = form.cleaned_data['sale_price_per_unit']
            Sale.objects.create(
                storage=storage,
                product=product,
                quantity=quantity,
                purchase_price_per_unit=purchase_price_per_unit,
                sale_price_per_unit=sale_price_per_unit
            )
            product.total_cost -= (quantity * purchase_price_per_unit)
            product.quantity -= quantity
            product.save()
        return redirect("/storage")