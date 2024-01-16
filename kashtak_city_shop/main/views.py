from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category, Order


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
