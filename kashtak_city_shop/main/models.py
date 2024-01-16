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
    SIZES_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'ExtraLarge'),
    )
    title = models.CharField(max_length=56, verbose_name='Название')
    price = models.FloatField(default=0, verbose_name='Цена')
    size = models.CharField(max_length=2, choices=SIZES_CHOICES, default=SIZES_CHOICES[0][0], verbose_name='Размер')
    quantity = models.IntegerField(default=0, verbose_name='Количество товара')
    product_description = models.TextField(verbose_name='Описание товара')
    model_description = models.TextField(verbose_name='Описание модели')
    delivery_description = models.TextField(verbose_name='Описание доставки')
    vendor_code = models.CharField(max_length=52, verbose_name='Артикул')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    gender = models.CharField(max_length=1, choices=GENDERS_CHOICES, default=GENDERS_CHOICES[0][0], verbose_name='Пол')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Order(models.Model):
    STATUS_CHOICES = (
        ('О', 'Оплачен'),
        ('С', 'Собирается'),
        ('От', 'Отправлен'),
        ('В', 'В пути'),
        ('Ж', 'Ждет получения'),
        ('П', 'Получен'),
    )
    products = models.ManyToManyField(Product, verbose_name='Товары')
    name = models.CharField(max_length=52, verbose_name='Имя')
    surname = models.CharField(max_length=52, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=52, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Email')
    phoneNumberRegex = RegexValidator(regex=r'^((\+\d{,4})[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, verbose_name='Номер телефона')
    region = models.CharField(max_length=52, verbose_name='Область')
    city = models.CharField(max_length=52, verbose_name='Город')
    street_name = models.CharField(max_length=52, verbose_name='Название улицы')
    house_number = models.IntegerField(default=0, verbose_name='Номер дома')
    entrance = models.IntegerField(default=0, verbose_name='Подъезд')
    floor = models.IntegerField(default=0, verbose_name='Этаж')
    apartment = models.IntegerField(default=0, verbose_name='Номер квартиры')
    post_code = models.IntegerField(default=0, verbose_name='Почтовый индекс')
    comment = models.TextField(max_length=300, verbose_name='Комментарий')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Заказчик')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], verbose_name='Статус')

    def __str__(self):
        return f'{self.name} {self.surname}'
