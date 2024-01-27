from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .forms import OrderCreateForm
from .models import Product, Category, Order, OrderItem, ProductSize
from cart.forms import CartAddProductForm

from cart.cart import Cart


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products_list'
    ordering = '-created'


class ProductCategoryListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products_list'
    ordering = '-created'

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category'])

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category_title'] = get_object_or_404(Category, slug=self.kwargs['category']).title
        return data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cart_form'] = CartAddProductForm(initial={'quantity': 1})
        return data


class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderCreateForm

    def form_valid(self, form):
        cart = Cart(self.request)
        instance = form.save()
        for item in cart:
            OrderItem.objects.create(
                order=instance,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
            product = item['product']
            product.quantity -= item['quantity']
            product.save()
        cart.clear()

        return redirect(reverse('order_created', kwargs={'pk': instance.id}))


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_created.html'
    context_object_name = 'order'
