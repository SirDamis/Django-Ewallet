from django import template
from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

class RegisterView(TemplateView):
    template_name = 'html/auth/register.html'


class LoginView(TemplateView):
    template_name = 'html/auth/login.html'

class ForgotPasswordView(TemplateView):
    template_name = 'html/auth/forgot-password.html'





class HomeView(TemplateView):
    template_name = 'html/home.html'