from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('remove/one/<int:pk>/', views.cart_remove_one_product_item, name='cart_remove_one_product_item'),
    path('remove/all/<int:pk>/', views.cart_remove_all_product_items, name='cart_remove_all_product_items'),

]
