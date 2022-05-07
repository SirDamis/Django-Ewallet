from django.urls import path

from .views import (
    FundWallet,
    ReceiveFundView,
    SendFundView,
    WalletView,
    TransactionView,
    WithdrawWalletView,
)

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
    path('send-fund/', SendFundView.as_view(), name='send-fund'),
    path('receive-fund/', ReceiveFundView.as_view(), name='receive-fund'),
    path('fund-wallet', FundWallet.as_view(), name='fund-wallet'),
    path('withdraw-wallet', WithdrawWalletView.as_view(), name='withdraw-wallet'),
] 
