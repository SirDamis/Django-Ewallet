from django.db import models
from django.conf import settings


class Referral(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    code = models.CharField(unique=True, max_length=16)
    number_of_users_referred = models.IntegerField(default=0)