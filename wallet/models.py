from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(decimal_places=2, max_digits=14)
    created_at = models.DateField(default=timezone.now)
    last_transaction = models.DateField(null=True)




class TransactionHistory(models.Model):
    reference = models.CharField(unique=True, max_length=16)
    amount = models.DecimalField(decimal_places=2, max_digits=14)
    details = models.TextField(null=True, default=None)
    date = models.DateField(default=timezone.now)
    TYPE_CHOICES=(
        ('FW', 'Fund Wallet'),
        ('WW', 'Withdaw Wallet'),
        ('TW', 'Transfer Wallet')
    )
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default='FW',
    )

    SUCCESS_CHOICES=(
        (True, 'True'),
        (False, 'False'),
    )
    success = models.BooleanField(default=False)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_by')
    to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_to')



class PendingWithdrawal(models.Model):
    reference = models.CharField(unique=True, max_length=16)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=16, default='PENDING')
    amount = models.DecimalField(decimal_places=2, max_digits=14)
    date = models.DateField(default=timezone.now)
