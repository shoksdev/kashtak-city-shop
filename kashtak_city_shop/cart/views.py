from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from main.forms import PromoCodeApplyForm
from main.models import PromoCode


def cart_add(request, pk):
    if request.method == 'POST':
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     size=cd['size'],
                     update_quantity=cd['update'])
        return redirect('cart_detail')


def cart_clear(request):
    Cart(request).clear()
    return redirect('cart_detail')


def cart_remove_one_product_item(request, pk):
    cart = Cart(request)
    cart.remove_one_product_item(pk)
    return redirect('cart_detail')


def cart_remove_all_product_items(request, pk):
    cart = Cart(request)
    cart.remove_all_product_items(pk)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'detail.html', {'cart': cart})


def promo_code_apply(request):
    if request.method == 'POST':
        form = PromoCodeApplyForm(request.POST)
        if form.is_valid():
            promo_code_from_form = form.cleaned_data['promo_code']
            try:
                promo_code = PromoCode.objects.get(promo_code=promo_code_from_form)
                request.session['promo_code_id'] = promo_code.id
            except:
                request.session['promo_code_id'] = None
        return redirect('order_create')
