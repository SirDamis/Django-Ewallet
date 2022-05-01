from django.db import models
from django.conf import settings
from pytz import timezone
from sqlalchemy import null


# class Wallet(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     balance = models.DecimalField()
#     created_at = models.DateField(default=timezone.now)
#     last_transaction = models.DateField(default=timezone.now)




# class TransactionHistory(models.Model):
#     reference = models.CharField()
#     details = models.CharField(null=True)
#     type = models.Choices()


