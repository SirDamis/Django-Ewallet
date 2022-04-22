from django import template
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from django.conf import settings
from .forms import RegisterForm

class RegisterView(CreateView):
    template_name = 'html/auth/register.html'


class LoginView(TemplateView):
    template_name = 'html/auth/login.html'

class ForgotPasswordView(TemplateView):
    template_name = 'html/auth/forgot-password.html'





class HomeView(TemplateView):
    template_name = 'html/home.html'