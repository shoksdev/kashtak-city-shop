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
        fields = ('first_name', 'last_name', 'username', 'email', 'avatar',)


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('region', 'city', 'street_name', 'house_number', 'entrance', 'floor', 'apartment', 'post_code',)
        widgets = {
            'region': forms.TextInput(attrs={'placeholder': 'Томская область'}),
            'city': forms.TextInput(attrs={'placeholder': 'Томск'}),
            'street_name': forms.TextInput(attrs={'placeholder': 'Мюниха'}),
            'house_number': forms.TextInput(attrs={'type': 'number', 'placeholder': '52'}),
            'entrance': forms.TextInput(attrs={'type': 'number', 'placeholder': '5'}),
            'floor': forms.TextInput(attrs={'type': 'number', 'placeholder': '2'}),
            'apartment': forms.TextInput(attrs={'type': 'number', 'placeholder': '52'}),
            'post_code': forms.TextInput(attrs={'type': 'number', 'placeholder': '524252'}),
        }
