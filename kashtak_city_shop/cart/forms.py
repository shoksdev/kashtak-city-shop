from django import forms


class CartAddProductForm(forms.Form):
    size = forms.CharField(max_length=2)
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={"class": "form-control w-25"}),
                                  label='Введите количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput, label='')
