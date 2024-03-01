from django.urls import path

from .views import ProductListView, ProductDetailView, OrderCreateView, \
    OrderDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category>/', ProductListView.as_view(), name='products_list_category'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/created/<int:pk>/', OrderDetailView.as_view(), name='order_created'),

]
