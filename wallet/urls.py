from django.urls import path

from .views import (
    WalletView
)

urlpatterns = [
    # path('/login', ),


    path('', WalletView.as_view(), name='Wallet'),
]
