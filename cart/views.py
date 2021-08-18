from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
# Create your views here.

from shop.models import Product
from .froms import AddProductForm
from .cart import Cart

def add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # data is delivered from client to server 
    # sql injection should be checked
    form = AddProductForm(request.POST)

    if form.is_vaild():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])

    return redirect('cart:detail')