from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .forms import OrderCreateFormForUserWithAddressAndInfo, \
    OrderCreateFormForUserWithAddress, OrderCreateFormForUserWithoutAll
from .models import Product, Category, Order, OrderItem, ProductSize, PromoCode
from cart.forms import CartAddProductForm, PromoCodeApplyForm

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

    def get_form_class(self):
        current_user = self.request.user
        if current_user.is_authenticated and current_user.region and current_user.first_name:
            return OrderCreateFormForUserWithAddressAndInfo
        elif current_user.is_authenticated and current_user.region:
            return OrderCreateFormForUserWithAddress
        else:
            return OrderCreateFormForUserWithoutAll

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

        if current_user.is_authenticated and current_user.region:
            instance.region = current_user.region
            instance.city = current_user.city
            instance.street_name = current_user.street_name
            instance.house_number = current_user.house_number
            instance.entrance = current_user.entrance
            instance.floor = current_user.floor
            instance.apartment = current_user.apartment
            instance.post_code = current_user.post_code
            instance.email = current_user.email
            instance.phone = current_user.phone
            if current_user.first_name:
                instance.name = current_user.first_name
                instance.surname = current_user.last_name
                instance.patronymic = current_user.patronymic

        instance.customer = current_user
        promo_code = cart.promo_code
        if promo_code:
            instance.promo_code = promo_code
            instance.total_sum = cart.get_total_price_after_discount()
        else:
            instance.total_sum = cart.get_total_price()

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

        size_ids_from_new_order = [item.get('size_id') for item in cart]
        product_quantities_from_new_order = [order_item.quantity for order_item in order_data_for_create]
        product_sizes = ProductSize.objects.filter(id__in=size_ids_from_new_order)

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
