from django.db import models
from user.models import User

class ReferralCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(unique=True, max_length=6)

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="referrer_user")
    referee =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="referee_user")