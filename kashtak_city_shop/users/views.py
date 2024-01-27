import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from main.models import Order

from .forms import RegistrationUserForm, InformationUpdateForm, AddressUpdateForm
from .models import CustomUser


class ProfileView(ListView, LoginRequiredMixin):
    context_object_name = 'orders_list'
    template_name = 'profile.html'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class CustomLoginView(LoginView):
    template_name = 'login.html'


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'


class RegistrationView(CreateView):
    form_class = RegistrationUserForm
    template_name = 'register.html'

    def form_valid(self, form):
        letters_for_code = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                            's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        random_code = [random.choice(letters_for_code) for letter in range(15)]

        instance = form.save(commit=False)
        email = self.request.POST.get('email')
        instance.username = email.lower().partition('@')[0]
        instance.referral_code = ''.join(random_code)
        instance.save()

        return redirect('login')


class InformationChangeView(UpdateView):
    model = CustomUser
    form_class = InformationUpdateForm
    template_name = 'information_change.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, id=self.request.user.id)


class AddressChangeView(UpdateView):
    model = CustomUser
    form_class = AddressUpdateForm
    template_name = 'address_change.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, id=self.request.user.id)
