from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from main.models import ProductSize


def cart_add(request, pk):
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            cart.add(product=product,
                     quantity=cd['quantity'],
                     size=cd['size'],
                     update_quantity=cd['update'])
        return redirect('cart_detail')


def cart_remove_all_product_items(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove_all_product_items(product)
    return redirect('cart_detail')


def cart_remove_one_product_item(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove_one_product_item(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'detail.html', {'cart': cart})
