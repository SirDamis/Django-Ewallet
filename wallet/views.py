from django import template
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

import rave_python.rave_exceptions as RaveExceptions
from ewallet.utils import generateTransactionReference, raveSetup, FLWSECK_TEST, FLWPUBK_TEST

import requests
from django.shortcuts import redirect



class WalletView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/dashboard.html'


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


    def verifyTransaction(response):
        if response['transactionComplete'] == True and  response['error'] == False:
            pass
            # Save to the transaction history database
            # Handle WaPay's transaction charge
            # Redirect with success prompt   

    def validateRaveCharge(response):
        rave = raveSetup()
        if response['validationRequired'] ==  True:
            validate_response = rave.Card.validate(
                response["flwRef"], "12345"
            )
            return validate_response

    

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
