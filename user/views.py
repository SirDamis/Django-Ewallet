from django import template
from django.http import request, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.conf import settings

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView


from .forms import RegisterForm

from .models import User
from wallet.models import Wallet

from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from ewallet.utils import account_activation_token
from .mixins import NotVerifiedDisallowedMixin

from django.contrib.sites.shortcuts import get_current_site


class HomeView(TemplateView):
    template_name = 'html/home.html'


# Sign Up View
class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'html/auth/register.html'
    success_url = reverse_lazy('login')
    success_message = "Account was created successfully"
    redirect_authenticated_user = True

    def form_valid(self, form):
        # obj = form.save(commit=False)
        # obj.referred_by = self.request.session['referral_code']
        # obj.save()

        return super(RegisterView, self).form_valid(form)

    def get(self, request, *args, **kwargs):

        current_site = get_current_site(request)
        # print(current_site)
        # print(request.session['referral_code'])
        if request.user.is_authenticated:
            return redirect('wallet')
        return super(RegisterView, self).get(self, request, *args, **kwargs)

class AccountNotVerifiedView(NotVerifiedDisallowedMixin, TemplateView):
    template_name = 'html/auth/account_not_verified.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_verified:
            return redirect('wallet')
        return super().get(self, request, *args, **kwargs)

class ActivateAccount(TemplateView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            # login(request, user)
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
            # messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid!')
            # messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')