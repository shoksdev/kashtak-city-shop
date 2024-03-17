from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class RegistrationUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2',)


class InformationUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic', 'username', 'email', 'avatar',)


class AddressUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('region', 'city', 'street_name', 'house_number', 'entrance', 'floor', 'apartment', 'post_code',)
        widgets = {
            'region': forms.TextInput(attrs={'placeholder': 'Томская область', 'required': True}),
            'city': forms.TextInput(attrs={'placeholder': 'Томск', 'required': True}),
            'street_name': forms.TextInput(attrs={'placeholder': 'Мюниха', 'required': True}),
            'house_number': forms.TextInput(attrs={'type': 'number', 'placeholder': '52', 'required': True}),
            'entrance': forms.TextInput(attrs={'type': 'number', 'placeholder': '5', 'required': True}),
            'floor': forms.TextInput(attrs={'type': 'number', 'placeholder': '2', 'required': True}),
            'apartment': forms.TextInput(attrs={'type': 'number', 'placeholder': '52', 'required': True}),
            'post_code': forms.TextInput(attrs={'type': 'number', 'placeholder': '524252', 'required': True}),
        }
