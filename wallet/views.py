from django import template
from django.views.generic import TemplateView


class WalletView(TemplateView):
    template_name = 'html/wallet/dashboard.html'



class SendFundView(TemplateView):
    template_name = 'html/wallet/send-fund.html'



class ReceiveFundView(TemplateView):
    template_name = 'html/wallet/receive-fund.html'



class FundWallet(TemplateView):
    template_name = 'html/wallet/'