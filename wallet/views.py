from django import template
from django.http import HttpResponse, request
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

import rave_python.rave_exceptions as RaveExceptions
from ewallet.utils import generateTransactionReference, raveSetup, FLWSECK_TEST, FLWPUBK_TEST

import requests
from django.shortcuts import redirect

from wallet.models import TransactionHistory, Wallet


class WalletView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/dashboard.html'

    def get_logged_in_user():
        return request.user

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            auth = self.request.user
            auth_wallet =  Wallet.objects.filter(user=auth).first()
            context['balance'] = auth_wallet.balance
            context['wallet_number'] = auth_wallet.number.hex
            return context
    

class RecordTransactionHistory:
    def __init__(self, reference, details, type, success, by, to):
        self.reference = reference
        self.details = details
        self.type = type
        self.success = success
        self.by = by
        self.to = to

    def save(self):
        TransactionHistory.objects.create(
            reference=self.reference,
            details=self.details,
            type=self.type,
            success=self.success,
            by=self.by,
            to=self.to,
        )


class TransactionView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/transaction.html'


class SendFundView(LoginRequiredMixin, TemplateView):
    """
    Send fund to another wallet.
    Allows for bunk transfer
    """
    login_url = '/login/'
    template_name = 'html/wallet/send-fund.html'

    

    def post(self, request, *args, **kwargs):
        wallet_number = request.POST.get('wallet_number')
        amount = request.POST.get('amount')
        details = request.POST.get('details')

        auth = self.request.user
        try:
            receiver_wallet = Wallet.objects.filter(number=wallet_number).first()
            sender_wallet = Wallet.objects.filter(user=auth).first()
            if sender_wallet.balance >= int(amount):
                tx_ref = generateTransactionReference()
                receiver_wallet.balance  += int(amount)
                sender_wallet.balance -= int(amount)
                receiver_wallet.save()
                sender_wallet.save()
                

                record_transaction = RecordTransactionHistory(
                    reference=tx_ref,
                    details=details,
                    type='Fund Wallet',
                    success=True,
                    by=auth,
                    to=receiver_wallet.user
                )
                record_transaction.save()

            else:
                return HttpResponse('balance not up amount being sent ')


        except ValidationError:
            return HttpResponse('Wallet Does Not exist')
        return HttpResponse('Deposit done')


class ReceiveFundView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/receive-fund.html'


class FundWallet(LoginRequiredMixin, TemplateView):
    """
    Fund the user wallet
    """
    login_url = '/login/'
    template_name = 'html/wallet/fund-wallet.html'

    def updateWallet(amount):
        # Get loggedin user and update ballance
        pass


    # def post(self, request, *args, **kwargs):
    #     amount = request.POST.get('amount')
    #     type = 'Fund Wallet'
    #     success = True
        
    #     # Update Wallet
    #     self.updateWallet(amount)



    def post(self, request, *args, **kwargs):
        json = {
            'tx_ref': generateTransactionReference(),
            'amount': int(request.POST.get('amount')),
            'currency': "NGN",
            'redirect_url': "http://127.0.0.1:8000/wallet",
            'customer': {
                'email': request.user.email,
                'name': request.user.name,
                'phone_number': "08102909304",
            }
        }
        response_data = requests.post(
            "https://api.flutterwave.com/v3/payments", 
            headers={'Authorization': 'Bearer '+FLWSECK_TEST},
            json=json
        ).json()
        if response_data['status'] == 'success':
            return redirect(response_data['data']['link'])
        return HttpResponse('Error') #Create error page



class WithdrawWalletView(LoginRequiredMixin, TemplateView):
    """
    Withdraw from user wallet to any bank account
    """
    login_url = '/login/'
    template_name = 'html/wallet/debit-wallet'
