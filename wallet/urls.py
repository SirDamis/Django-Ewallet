from django.urls import path

from .views import (
    FundWalletProccessView,
    FundWalletView,
    ReceiveFundView,
    SendFundView,
    WalletView,
    TransactionView,
    WithdrawWalletView,

    withdraw_wallet_status
)

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),
    path('transactions/', TransactionView.as_view(), name='transactions'),
    path('send-fund/', SendFundView.as_view(), name='send-fund'),
    path('receive-fund/', ReceiveFundView.as_view(), name='receive-fund'),
    path('fund-wallet/', FundWalletView.as_view(), name='fund-wallet'),
    path('fund-wallet/success/', FundWalletProccessView.as_view(), name='fund-wallet-success'),
    path('withdraw-wallet/', WithdrawWalletView.as_view(), name='withdraw-wallet'),
    path('withdraw-wallet/status/', withdraw_wallet_status, name='withdraw-wallet-status'),
] 
