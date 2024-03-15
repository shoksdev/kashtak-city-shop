from django.contrib import admin

from .models import Category, Product, Order, ProductImage, OrderItem, ProductSize, PromoCode


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage


class ProductSizeInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductSize


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'vendor_code')
    inlines = [ProductImageInline, ProductSizeInline]


class OrderItemInline(admin.TabularInline):
    fk_name = 'order'
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'phone', 'city', 'street_name')
    inlines = [OrderItemInline, ]


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'change_type', 'price_reduction', 'activation_quantity', )