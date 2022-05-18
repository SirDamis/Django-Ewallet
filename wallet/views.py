from decimal import Decimal
from django import template
from django.http import HttpResponse, request
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

import rave_python.rave_exceptions as RaveExceptions
from ewallet.utils import generateTransactionReference, raveSetup, FLWSECK_TEST

import requests
from django.shortcuts import redirect
from django.template.loader import render_to_string

from wallet.models import TransactionHistory, Wallet

class RecordTransactionHistory:
    def __init__(self, reference, details, type, success, by, to, amount):
        self.reference = reference
        self.details = details
        self.type = type
        self.success = success
        self.by = by
        self.to = to
        self.amount = amount

    def save(self):
        TransactionHistory.objects.create(
            reference=self.reference,
            details=self.details,
            type=self.type,
            success=self.success,
            by=self.by,
            to=self.to,
            amount=self.amount
        )


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
            if sender_wallet.balance >= float(amount) and float(amount) >= 0:
                tx_ref = generateTransactionReference()
                receiver_wallet.balance  += float(amount)
                sender_wallet.balance -= float(amount)
                receiver_wallet.save()
                sender_wallet.save()
                
                record_transaction = RecordTransactionHistory(
                    reference=tx_ref,
                    details=details,
                    amount=amount,
                    type='TW',
                    success=True,
                    by=auth,
                )
                record_transaction.save()
                
            elif float(amount) < 0:
                context = {'error_msg': 'Enter positive amount'}
                rendered = render_to_string('html/wallet/failed-fund.html', context=context)
                return HttpResponse(rendered)

            else:
                context = {'error_msg': 'Insufficient Fund'}
                rendered = render_to_string('html/wallet/failed-fund.html', context=context)
                return HttpResponse(rendered)


        except ValidationError:
            return HttpResponse('Wallet Does Not exist')
        return HttpResponse('Deposit done')


class ReceiveFundView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/receive-fund.html'

class FundWalletProccessView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/successful-fund.html'

    def get(self, request, *args, **kwargs):
        print(self.request.GET.get('status'))
        if self.request.GET.get('status') == 'successful':
            tx_ref = self.request.GET.get('tx_ref')
            transactionDetails = TransactionHistory.objects.filter(reference=tx_ref).first()
            auth = self.request.user
            wallet = Wallet.objects.filter(user=auth).first()
          
            try:
                response =  raveSetup().Card.verify(tx_ref)
                if response['transactionComplete'] == True and response['amount'] == float(transactionDetails.amount) and transactionDetails.success == False:
                    wallet.balance  += Decimal(transactionDetails.amount)
                    transactionDetails.success == 'True'
                    wallet.save()
                    transactionDetails.save()
                else:
                    context = {'error_msg': 'Transaction Already Performed'}
                    rendered = render_to_string('html/wallet/failed-fund.html', context=context)
                    return HttpResponse(rendered)
            except RaveExceptions.TransactionVerificationError:
                context = {'error_msg': 'Unable to verify transaction'}
                rendered = render_to_string('html/wallet/failed-fund.html', context=context)
                return HttpResponse(rendered)
        else:
            return redirect('fund-wallet')


class FundWalletView(LoginRequiredMixin, TemplateView):
    """
    Fund the user wallet
    """
    login_url = '/login/'
    template_name = 'html/wallet/fund-wallet.html'

    def post(self, request, *args, **kwargs):
        tx_ref = generateTransactionReference()
        auth = self.request.user
        amount = float(request.POST.get('amount'))

        json = {
            'tx_ref': tx_ref,
            'amount': amount,
            'currency': "NGN",
            'redirect_url': "http://127.0.0.1:8000/wallet/fund-wallet/succes",
            'customer': {
                'email': request.user.email,
                'name': request.user.name,
            }
        }
        response_data = requests.post(
            "https://api.flutterwave.com/v3/payments", 
            headers={'Authorization': 'Bearer '+FLWSECK_TEST},
            json=json
        ).json()

        if response_data['status'] == 'success':
            record_transaction = RecordTransactionHistory(
                reference=tx_ref,
                amount = amount,
                details='Fund Wallet',
                type='FW',
                success=False,
                by=auth,
                to=auth
            )
            record_transaction.save()
            return redirect(response_data['data']['link'])
        return HttpResponse('Error') #Create error page



class WithdrawWalletView(LoginRequiredMixin, TemplateView):
    """
    Withdraw from user wallet to any bank account
    """
    login_url = '/login/'
    template_name = 'html/wallet/debit-wallet'
