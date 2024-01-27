from django.urls import path, reverse_lazy

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/information/change/', views.InformationChangeView.as_view(), name='information_change'),
    path('profile/address/change/', views.AddressChangeView.as_view(), name='address_change'),
    path('profile/password/change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html',
                                                                           success_url=reverse_lazy('profile')),
         name='password_change'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
]
