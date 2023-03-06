from django.urls import path

from .views import (
   ReferralView
)

urlpatterns = [
    path('', ReferralView.as_view(), name='wallet'),
    # path('fund-wallet/success/', FundWalletProccessView.as_view(), name='fund-wallet-success'),
] 
