from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    # name = forms.CharField(label='name', required=True)
    # email = forms.EmailField(label='email', required=True)
    # password = forms.CharField(label='password', widget=forms.PasswordInput()) 
    # password_confirmation = forms.CharField(label='password_confirmation', widget=forms.PasswordInput())


    class Meta:
        model = settings.AUTH_USER_MODEL
        field = ['name', 'email', 'password']


