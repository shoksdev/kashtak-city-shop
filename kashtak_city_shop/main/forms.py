from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('name', 'surname', 'patronymic', 'email', 'phone', 'region', 'city', 'street_name', 'house_number',
                  'entrance', 'floor', 'apartment', 'post_code', 'comment')
