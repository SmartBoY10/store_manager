from django.shortcuts import render
from .models import *

def get_list(request):
    products = Product.objects.all()
    return render(request, "store_app/index.html", {"product_list":products})
