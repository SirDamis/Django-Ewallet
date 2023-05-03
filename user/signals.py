import string
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from wallet.models import Wallet
from referral.models import ReferralCode

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string


from django.core.mail import EmailMessage
from ewallet.utils import account_activation_token
from django.contrib.sites.models import Site

import random

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        current_site = Site.objects.get_current().domain
        mail_subject = 'Activate your blog account.'
        message = render_to_string('emails/activate_account.html', {
            'user': instance,
            'domain': current_site,
            'uid':urlsafe_base64_encode(force_bytes(instance.pk)),
            'token':account_activation_token.make_token(instance),
        })
        to_email = instance.email

        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=0.0)

def generate_referral_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_user_referral_code(sender, instance, created, **kwargs):
    code = generate_referral_code()
    if created:
        ReferralCode.objects.create(user=instance, code=code)