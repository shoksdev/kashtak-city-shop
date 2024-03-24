from django import forms

from .models import Order


class OrderCreateFormForUserWithoutAll(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'surname', 'patronymic', 'email', 'phone', 'region', 'city', 'street_name', 'house_number',
                  'entrance', 'floor', 'apartment', 'post_code', 'comment',)


class OrderCreateFormForUserWithAddress(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'surname', 'patronymic', 'phone', 'comment',)


class OrderCreateFormForUserWithAddressAndInfo(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('comment',)