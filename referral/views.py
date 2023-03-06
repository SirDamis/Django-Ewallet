from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from user.mixins import VerificationRequiredMixin

from django.views.generic import TemplateView
from .models import Referral
from user.models import User

class CreateUserReferralDetails:
    def generateCode():
        code = 'X4q5dQe'
        while Referral.objects.filter(code).exists:
            code = 'LKSDM'
        return code

    def __init__(self, user):
        self.user = user
        self.code = self.generateCode()
        self.number_of_users_referred = 0

    def save(self):
        Referral.objects.create(
            user=self.user,
            code=self.code,
            number_of_users_referred=self.number_of_users_referred
        )

class ReferralView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/referral/home.html'

    def fetch_referred_users(self, auth):
        try:
            all_referred_users = User.objects.get(referred_by=auth.pk)
        except User.DoesNotExist:
            all_referred_users = User.objects.none()
        return all_referred_users


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_referral = Referral.objects.filter(user=auth).first()

        context['auth_referred_user'] = self.fetch_referred_users(auth)
        context['auth_referral_code'] = auth_referral.code
        context['auth_referral_total'] = auth_referral.number_of_users_referred
        return context
    
    def get(self, request, *args, **kwargs):
        auth = self.request.user
        auth_referral = Referral.objects.filter(user=auth).first()
        if not auth_referral:
            create_referral = CreateUserReferralDetails(auth)
            create_referral.save()
        return super().get(self, request, *args, **kwargs)

from django.forms.models import model_to_dict
class ReferralRegistrationView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        code = self.kwargs['code']
        result = Referral.objects.filter(code=code).first()
        
        if result:
            # request.session['referral_code'] = model_to_dict(result)
            return HttpResponse(request.session['referral_code'] )
            # return redirect('register')
        else:
            return HttpResponse('Invalid Code')
        return super().dispatch(request, *args, **kwargs)
        
