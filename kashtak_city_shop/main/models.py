from django.core.validators import RegexValidator
from django.db import models

from users.models import CustomUser


class Category(models.Model):
    title = models.CharField(max_length=52, verbose_name='Название')
    slug = models.SlugField(max_length=100, db_index=True, verbose_name='URL slug')

    def __str__(self):
        return self.title


class Product(models.Model):
    GENDERS_CHOICES = (
        ('М', 'Мужское'),
        ('Ж', 'Женское'),
    )
    title = models.CharField(max_length=56, verbose_name='Название')
    price = models.FloatField(default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество товара')
    product_description = models.TextField(verbose_name='Описание товара')
    model_description = models.TextField(verbose_name='Описание модели')
    delivery_description = models.TextField(verbose_name='Описание доставки')
    vendor_code = models.CharField(max_length=52, verbose_name='Артикул')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    gender = models.CharField(max_length=1, choices=GENDERS_CHOICES, default=GENDERS_CHOICES[0][0], verbose_name='Пол')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    def get_product_in_stock(self):
        sizes = ProductSize.objects.filter(product=self.id)
        quantity_flag = False
        for size in sizes:
            if size.quantity > 0:
                quantity_flag = True
                break

        return quantity_flag

    def __str__(self):
        return self.title


class ProductSize(models.Model):
    SIZES_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'ExtraLarge'),
    )
    size = models.CharField(max_length=2, choices=SIZES_CHOICES, default=SIZES_CHOICES[0][0], verbose_name='Размер')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes', verbose_name='Товар')

    def __str__(self):
        return self.size


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')


class Order(models.Model):
    STATUS_CHOICES = (
        ('О', 'Оплачен'),
        ('С', 'Собирается'),
        ('От', 'Отправлен'),
        ('В', 'В пути'),
        ('Ж', 'Ждет получения'),
        ('П', 'Получен'),
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True,
                                 verbose_name='Заказчик')
    name = models.CharField(max_length=52, verbose_name='Имя')
    surname = models.CharField(max_length=52, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=52, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Email')
    phoneNumberRegex = RegexValidator(regex=r'^((\+\d{,4})[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, verbose_name='Номер телефона')
    region = models.CharField(max_length=52, verbose_name='Область')
    city = models.CharField(max_length=52, verbose_name='Город')
    street_name = models.CharField(max_length=52, verbose_name='Название улицы')
    house_number = models.IntegerField(verbose_name='Номер дома')
    entrance = models.IntegerField(verbose_name='Подъезд')
    floor = models.IntegerField(verbose_name='Этаж')
    apartment = models.IntegerField(verbose_name='Номер квартиры')
    post_code = models.IntegerField(verbose_name='Почтовый индекс')
    comment = models.TextField(max_length=300, blank=True, null=True, verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], verbose_name='Статус')

    def calculate_total_sum(self):
        total_sum = 0
        items = OrderItem.objects.filter(order_id=self.id).values('price', 'quantity')
        for item in items:
            item_sum = item['price'] * item['quantity']
            total_sum += item_sum
        return total_sum

    def __str__(self):
        return f'{self.name} {self.surname}'


class OrderItem(models.Model):
    SIZES_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'ExtraLarge'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    size = models.CharField(max_length=2, choices=SIZES_CHOICES, default=SIZES_CHOICES[0][0], verbose_name='Размер')

    def calculate_product_total_sum(self):
        return self.quantity * self.price

    def __str__(self):
        return f'Order Item №{self.id}'
