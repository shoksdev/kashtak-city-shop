from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    phoneNumberRegex = RegexValidator(regex=r'^((\+\d{,4})[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, blank=True, null=True,
                             verbose_name='Номер телефона')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Изображение', )
    referral_code = models.CharField(max_length=104, verbose_name='Реферальный код')
    bonuses = models.IntegerField(default=0, verbose_name='Бонусы')

    region = models.CharField(max_length=52, blank=True, null=True, verbose_name='Область')
    city = models.CharField(max_length=52, blank=True, null=True, verbose_name='Город')
    street_name = models.CharField(max_length=52, blank=True, null=True, verbose_name='Название улицы')
    house_number = models.IntegerField(blank=True, null=True, verbose_name='Номер дома')
    entrance = models.IntegerField(blank=True, null=True, verbose_name='Подъезд')
    floor = models.IntegerField(blank=True, null=True, verbose_name='Этаж')
    apartment = models.IntegerField(blank=True, null=True, verbose_name='Номер квартиры')
    post_code = models.IntegerField(blank=True, null=True, verbose_name='Почтовый индекс')

    def __str__(self):
        return self.username
