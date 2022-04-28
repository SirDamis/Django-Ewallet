from django import template
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from django.conf import settings
# from .forms import RegisterForm

# class RegisterView(CreateView):
#     template_name = 'html/auth/register.html'

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginForm, RegisterForm

# Sign Up View
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'html/auth/register.html'
    success_url = reverse_lazy('login')


# class LoginView(TemplateView):
#     form_class = LoginForm
#     template_name = 'html/auth/login.html'
#     success_url = reverse_lazy('dashboard')

class ForgotPasswordView(TemplateView):
    template_name = 'html/auth/forgot-password.html'





class HomeView(TemplateView):
    template_name = 'html/home.html'