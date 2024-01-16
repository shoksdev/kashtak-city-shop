from django.urls import path

from .views import ProductListView, ProductDetailView, ProductCategoryListView

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:category>/', ProductCategoryListView.as_view(), name='products_list_category'),
]
