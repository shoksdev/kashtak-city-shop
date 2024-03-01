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
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.product_ids = set()
        for cart_item in self.cart.values():
            self.product_ids.add(int(cart_item.get('product_id')))

    def add(self, product, size, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """

        product_id = product.id

        new_cart_item = {'product_id': product_id, 'quantity': quantity, 'size': size, 'price': str(product.price)}

        if not bool(self.cart):
            last_key = 0
        else:
            last_key = int(max(self.cart))
        if product_id not in self.product_ids:
            self.cart[last_key + 1] = new_cart_item
        else:
            flag = False
            cart_item_position = None
            for cart_item in range(1, len(self.cart) + 1):
                cart_item_str = str(cart_item)
                if self.cart[cart_item_str]['product_id'] == product_id and update_quantity:
                    self.cart[cart_item_str]['quantity'] = quantity
                    break
                elif self.cart[cart_item_str]['product_id'] == product_id and self.cart[cart_item_str]['size'] == size:
                    flag, cart_item_position = False, cart_item_str
                    break
                elif self.cart[cart_item_str]['product_id'] == product_id and self.cart[cart_item_str]['size'] != size:
                    flag = True
            if flag:
                self.cart[last_key + 1] = new_cart_item
            else:
                self.cart[cart_item_position]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove_all_product_items(self, cart_item_id):
        del self.cart[str(cart_item_id)]
        self.save()

    def remove_one_product_item(self, cart_item_id):
        """
        Удаление одного товара из корзины.
        """
        cart_item = self.cart[str(cart_item_id)]
        if cart_item['quantity'] <= 1:
            del self.cart[str(cart_item_id)]
        else:
            cart_item['quantity'] -= 1
        self.save()

    def all_products(self):
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=self.product_ids).values_list(flat=True)
        return products

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=self.product_ids)
        for value in self.cart.values():
            product = products.get(id=value['product_id'])
            value['product'] = product

        for key, value in self.cart.items():
            value['price'] = Decimal(value['price'])
            value['total_price'] = value['price'] * value['quantity']
            value['id'] = key
            yield value

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
