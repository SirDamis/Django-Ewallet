from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wallet.models import Wallet

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string


from django.core.mail import EmailMessage
from ewallet.utils import account_activation_token
from django.contrib.sites.models import Site



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        current_site = 'www.hello.com'
        mail_subject = 'Activate your blog account.'
        message = render_to_string('emails/activate_account.html', {
            'user': instance,
            'domain': current_site,
            'uid':urlsafe_base64_encode(force_bytes(instance.pk)),
            'token':account_activation_token.make_token(instance),
        })
        to_email = instance.email
        print(to_email)
        print(message)
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=0.0)








# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
            
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})