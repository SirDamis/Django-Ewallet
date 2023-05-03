from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Referral, ReferralCode
from user.models import User
from user.signals import generate_referral_code

from .forms import RegisterForm
from django.contrib import messages

class ReferralView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/referral/home.html'

    def fetch_referred_users(self):
        all_referred_users = Referral.objects.filter(referrer=self.request.user)
        return all_referred_users
    
    def auth_referrer_code(self):
        try:
            referral_code = ReferralCode.objects.get(user=self.request.user).code
        except ReferralCode.DoesNotExist:
            referral_code = generate_referral_code()
            ReferralCode.objects.create(user=self.request.user, code=referral_code)
        return referral_code
    
    def number_of_users_referred(self):
        no_referred = Referral.objects.filter(referrer=self.request.user).count()
        return no_referred

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        context['auth_referred_user'] = self.fetch_referred_users()
        context['auth_referral_code'] = self.auth_referrer_code()
        context['auth_referral_total'] = self.number_of_users_referred()
        return context
    
    # def get(self, request, *args, **kwargs):
    #     auth = self.request.user
    #     auth_referral = Referral.objects.filter(user=auth).first()
    #     if not auth_referral:
    #         create_referral = CreateUserReferralDetails(auth)
    #         create_referral.save()
    #     return super().get(self, request, *args, **kwargs)

# class ReferralRegistrationView(TemplateView):
#     form_class = RegisterForm
#     template_name = 'html/referral/join-us.html'
#     success_url = reverse_lazy('login')
#     success_message = "Account was created successfully"
#     redirect_authenticated_user = True

#     def dispatch(self, request, *args, **kwargs):
#         try:
#             self.referral_detail = ReferralCode.objects.get(code=self.kwargs['code'])
#         except ReferralCode.DoesNotExist:
#             messages.error(request, "Invalid referral code!!")
#             return redirect(reverse('register')) 
#         return super(ReferralRegistrationView, self).dispatch(request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         context = {
#             'form': form, 
#             'referral_code': self.kwargs['code'],
#             'referral_name': self.referral_detail.user.name,
#         }
#         return render(request, self.template_name, context)





from django.views.generic.edit import FormView

class ReferralRegistrationView(FormView):
    form_class = RegisterForm
    template_name = 'html/referral/join-us.html'
    success_url = reverse_lazy('login')
    success_message = "Account was created successfully"
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        try:
            self.referral_detail = ReferralCode.objects.get(code=self.kwargs['code'])
        except ReferralCode.DoesNotExist:
            messages.error(request, "Invalid referral code!!")
            return redirect(reverse('register')) 
        return super(ReferralRegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        referral = Referral.objects.create(referrer=self.referral_detail.user, referee=user)
        print("I am here")
        referral.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referral_code'] = self.kwargs['code']
        context['referral_name'] = self.referral_detail.user.name
        return context
