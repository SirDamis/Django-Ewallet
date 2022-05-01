from django import template
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

class WalletView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/dashboard.html'

class TransactionView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/transaction.html'



class SendFundView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/send-fund.html'


class ReceiveFundView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/receive-fund.html'


class FundWallet(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/fund-wallet'

# class DebitWallet(LoginRequiredMixin, TemplateView):
#     login_url = '/login/'
#     template_name = 'html/wallet/debit-wallet'