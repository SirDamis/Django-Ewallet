from django import template
from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

class RegisterView(CreateView):
    template_name = 'html/auth/login.html'






class HomeView(TemplateView):
    template_name = 'html/home.html'