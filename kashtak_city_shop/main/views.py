from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .forms import OrderCreateForm, PromoCodeApplyForm
from .models import Product, Category, Order, OrderItem, ProductSize, PromoCode
from cart.forms import CartAddProductForm

from cart.cart import Cart


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products_list'
    ordering = '-created'

    def get_queryset(self):
        category = self.kwargs.get('category', None)
        if category is not None:
            return Product.objects.filter(category__slug=category)
        else:
            return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        category = self.kwargs.get('category', None)
        data = super().get_context_data(**kwargs)
        if category is not None:
            data['category_title'] = get_object_or_404(Category, slug=category).title
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

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['promo_code_apply_form'] = PromoCodeApplyForm()
        return data

    def form_valid(self, form):
        cart = Cart(self.request)
        bonuses_for_user = cart.get_total_price() / 10
        current_user = self.request.user
        current_user.bonuses += bonuses_for_user
        current_user.save()
        order_data_for_create, product_sizes_data_for_update = [], []
        instance = form.save(commit=False)
        instance.promo_code = cart.promo_code
        instance.total_sum = cart.get_total_price_after_discount()
        instance.customer = current_user
        instance.save()
        for item in cart:
            item_product = item.get('product')
            item_size = item.get('size')
            item_quantity = item.get('quantity')
            item_price = item.get('price')
            order_data_for_create.append(
                OrderItem(
                    order=instance,
                    product=item_product,
                    price=item_price,
                    quantity=item_quantity,
                    size=item_size
                ))

        product_ids_from_new_order = [item.get('product_id') for item in cart]
        product_sizes_from_new_order = [item.get('size') for item in cart]
        product_quantities_from_new_order = [order_item.quantity for order_item in order_data_for_create]

        product_sizes = ProductSize.objects.filter(product__in=product_ids_from_new_order,
                                                   size__in=product_sizes_from_new_order)

        for size in range(len(product_sizes)):
            product_sizes_data_for_update.append(
                ProductSize(
                    id=product_sizes[size].id,
                    quantity=product_sizes[size].quantity - product_quantities_from_new_order[size]
                )
            )
        ProductSize.objects.bulk_update(product_sizes_data_for_update, ['quantity'])

        OrderItem.objects.bulk_create(order_data_for_create)

        cart.clear()

        return redirect(reverse('order_created', kwargs={'pk': instance.id}))


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_created.html'
    context_object_name = 'order'
