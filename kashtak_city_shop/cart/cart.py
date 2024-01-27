from decimal import Decimal
from django.conf import settings
from main.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = []
        self.cart = cart

    def add(self, product, size, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """

        # for cart_item in cart:
        #     if cart_item_new['product_id'] == cart_item['product_id'] and cart_item['size'] == cart_item_new['size']:
        #         cart_item['quantity'] += cart_item_new['quantity']
        #         break
        #     else:
        #         cart.append(cart_item_new)
        #         break
        product_id = str(product.id)
        print(self.cart)
        # if product_id not in self.cart:
        #     self.cart[product_id] = {'product_id': product_id, 'quantity': 0, 'size': size, 'price': str(product.price)}
        # if update_quantity:
        #     self.cart[product_id]['quantity'] = quantity
        # else:
        #     self.cart[product_id]['quantity'] += quantity
        # self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove_all_product_items(self, product):
        """
        Удаление всего товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def remove_one_product_item(self, product):
        """
        Удаление одного товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            self.save()

    def all_products(self):
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids).values_list(flat=True)
        return products

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def len(self):
        """
        Подсчет всех товаров в корзине.
        """
        return len(self.cart)

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
