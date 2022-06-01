from django import template
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from django.conf import settings
from wallet.models import Wallet
# from .forms import RegisterForm

# class RegisterView(CreateView):
#     template_name = 'html/auth/register.html'

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterForm
from .models import User
from django.contrib.messages.views import SuccessMessageMixin

# Sign Up View
class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'html/auth/register.html'
    success_url = reverse_lazy('login')
    success_message = "Account was created successfully"
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('wallet')
        return super(RegisterView, self).get(self, request, *args, **kwargs)





class HomeView(TemplateView):
    template_name = 'html/home.html'
