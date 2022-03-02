from django.shortcuts import redirect, render
from django.views.generic.base import View

from .models import *
from .forms import *


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
        cart_total_price = 0
        s = request.session
        try:
            buyer = Buyer.objects.get(session_id=s.session_key)
            orders = Order.objects.filter(buyer_id=buyer.id)
        except:
            b = "Buyer not found"

        if b == "Buyer not found":
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
            order.total_price = order.product.price * quantity
            order.save()

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
            status = Status.objects.get(status_type='NOT_SERVED')
            pay_type = PayType.objects.get(pay_type=form.cleaned_data['pay_type'])

            orders_dict = {}
            for order in orders:
                orders_dict[order.id] = {
                                        "Product": order.product.name, 
                                        "Quantity": order.quantity, 
                                        "Total price": order.total_price
                                        }

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
            
            