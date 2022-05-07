from django import template
from django.http import request
from django.shortcuts import redirect, render
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
from .forms import RegisterForm
from .models import User

# Sign Up View
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'html/auth/register.html'
    success_url = reverse_lazy('login')
    redirect_authenticated_user = True

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('wallet')
    #     return super(RegisterView, self).dispatch(self, request, *args, **kwargs)





class HomeView(TemplateView):
    template_name = 'html/home.html'
    