from unicodedata import name
from django.urls import path

from .views import (
    WalletView,
    TransactionView
)

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('transactions', TransactionView.as_view(), name='transactions')
]
