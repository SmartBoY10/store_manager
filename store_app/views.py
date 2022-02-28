from django.shortcuts import redirect, render
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


class AddToCart(View):
    def get(self, request, pk):
        b = ""
        o = ""
        s = request.session
        product = Product.objects.get(id=pk)
        try:
            buyer = Buyer.objects.get(session_id=s.session_key)
            cart = Cart.objects.get(buyer_id=buyer.id)
            try:
                order = Order.objects.get(product_id=product.id, buyer_id=buyer.id)
                order.quantity += 1
                order.total_price += product.price
                order.save()
            except:
                o = "order not found"

            if o == "order not found":
                order = Order.objects.create(buyer=buyer, product=product, quantity=1, total_price=product.price, cart=cart)

        except:
            b = "Not found"
        
        if b == "Not found":
            buyer = Buyer.objects.create(session_id=s.session_key)
            cart = Cart.objects.create(buyer=buyer)
            order = Order.objects.create(buyer=buyer, product=product, quantity=1, total_price=product.price, cart=cart)

        return redirect("/cart-detail")


class CartDetailView(View):
    def get(self, request):
        b = ""
        s = request.session
        try:
            buyer = Buyer.objects.get(session_id=s.session_key)
            orders = Order.objects.filter(buyer_id=buyer.id)
        except:
            b = "Buyer not found"

        if b == "Buyer not found":
            buyer = Buyer.objects.create(session_id=s.session_key)
            cart = Cart.objects.create(buyer=buyer)
            orders = Order.objects.filter(buyer_id=buyer.id)

        context = {'orders': orders}
        return render(request, "store_app/cart_detail.html", context)