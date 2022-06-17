from decimal import Decimal
import json
from django import template
from django.http import HttpResponse, request
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Sum

import rave_python.rave_exceptions as RaveExceptions
from ewallet.utils import generateTransactionReference, raveSetup, FLWSECK_TEST

import requests
from django.shortcuts import redirect
from django.template.loader import render_to_string

from wallet.models import TransactionHistory, Wallet


rave = raveSetup()


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        transaction_times = TransactionHistory.objects.filter(by=auth).count()
        amount_sent = TransactionHistory.objects.filter(
            by=auth, success=True, type='TW').aggregate(total_amount_sent=Sum('amount'))
        amount_received = TransactionHistory.objects.filter(
            to=auth, success=True, type='TW').aggregate(total_amount_received=Sum('amount'))
        transactions = (TransactionHistory.objects.filter(
            by=auth, success=True).order_by('-date')[:5])

        context['transactions'] = transactions
        context['amount_sent'] = amount_sent['total_amount_sent'] if amount_sent['total_amount_sent'] else 0
        context['amount_received'] = amount_received['total_amount_received'] if amount_received['total_amount_received'] else 0
        context['transaction_times'] = transaction_times
        context['balance'] = auth_wallet.balance
        context['wallet_number'] = auth_wallet.number.hex

        return context


class SendFundView(LoginRequiredMixin, TemplateView):
    """
    Send fund to another wallet.
    Allows for bunk transfer
    """
    login_url = '/login/'
    template_name = 'html/wallet/send-fund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['wallet_number'] = auth_wallet.number.hex
        return context

    def post(self, request, *args, **kwargs):
        wallet_number = request.POST.get('wallet_number')
        amount = request.POST.get('amount')
        details = request.POST.get('details')

        auth = self.request.user
        try:
            receiver_wallet = Wallet.objects.filter(
                number=wallet_number).first()
            sender_wallet = Wallet.objects.filter(user=auth).first()
            if sender_wallet.balance >= Decimal(amount) and Decimal(amount) >= 0:
                tx_ref = generateTransactionReference()
                receiver_wallet.balance += Decimal(amount)
                sender_wallet.balance -= Decimal(amount)
                receiver_wallet.save()
                sender_wallet.save()

                record_transaction = RecordTransactionHistory(
                    reference=tx_ref,
                    details=details,
                    amount=amount,
                    type='TW',
                    success=True,
                    by=auth,
                    to=receiver_wallet.user
                )
                record_transaction.save()

            elif float(amount) < 0:
                context = {'error_msg': 'Enter positive amount'}
                rendered = render_to_string(
                    'html/wallet/failed-fund.html', context=context)
                return HttpResponse(rendered)

            else:
                context = {'error_msg': 'Insufficient Fund'}
                rendered = render_to_string(
                    'html/wallet/failed-fund.html', context=context)
                return HttpResponse(rendered)

        except ValidationError:
            return HttpResponse('Wallet Does Not exist')

        context = {'error_msg': 'Deposit succcessful'}
        rendered = render_to_string(
            'html/wallet/successful-fund.html', context=context)
        return HttpResponse(rendered)


class ReceiveFundView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/receive-fund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['wallet_number'] = auth_wallet.number.hex
        return context

    # To Do:
    # -Barcode Display
    # -Share to Whatsapp, Twitter
    # -Custom Pay URL


class FundWalletProccessView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/successful-fund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['wallet_number'] = auth_wallet.number.hex
        return context

    # http://127.0.0.1:8000/wallet/fund-wallet/succes?status=successful&tx_ref=WP-1653008174132&transaction_id=3393442

    def get(self, request, *args, **kwargs):
        print(self.request.GET.get('status'))
        if (self.request.GET.get('status') == 'successful') and (self.request.GET.get('tx_ref')) and (self.request.GET.get('transaction_id')):
            tx_ref = self.request.GET.get('tx_ref')
            transactionDetails = TransactionHistory.objects.filter(
                reference=tx_ref).first()
            auth = self.request.user
            wallet = Wallet.objects.filter(user=auth).first()

            try:
                response = raveSetup().Card.verify(tx_ref)
                if response['transactionComplete'] == True and response['amount'] == float(transactionDetails.amount) and transactionDetails.success == False:
                    wallet.balance += Decimal(transactionDetails.amount)
                    wallet.save()

                    transactionDetails.success = True
                    transactionDetails.save()
                else:
                    # To do render the payment information
                    context = {'error_msg': 'Transaction Already Performed'}
                    rendered = render_to_string(
                        'html/wallet/failed-fund.html', context=context)
                    return HttpResponse(rendered)
            except RaveExceptions.TransactionVerificationError:
                context = {'error_msg': 'Unable to verify transaction'}
                rendered = render_to_string(
                    'html/wallet/failed-fund.html', context=context)
                return HttpResponse(rendered)
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect('fund-wallet')


class FundWalletView(LoginRequiredMixin, TemplateView):
    """
    Fund the user wallet
    """
    login_url = '/login/'
    template_name = 'html/wallet/fund-wallet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['wallet_number'] = auth_wallet.number.hex
        return context

    def post(self, request, *args, **kwargs):
        tx_ref = generateTransactionReference()
        auth = self.request.user
        amount = float(request.POST.get('amount'))

        json = {
            'tx_ref': tx_ref,
            'amount': amount,
            'currency': "NGN",
            'redirect_url': "http://127.0.0.1:8000/wallet/fund-wallet/success",
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
                amount=amount,
                details='Fund Wallet',
                type='FW',
                success=False,
                by=auth,
                to=auth
            )
            record_transaction.save()
            return redirect(response_data['data']['link'])
        return HttpResponse('Error')  # Create error page


class WithdrawWalletView(LoginRequiredMixin, TemplateView):
    """
    Withdraw from user wallet to any bank account
    """
    login_url = '/login/'
    template_name = 'html/wallet/withdraw-wallet.html'

    def charge(self):
        response_data = requests.get(
            "https://api.flutterwave.com/v3/transfers/rates",
            headers={'Authorization': 'Bearer '+FLWSECK_TEST},
            json={
                'amount': 100,
                'destination_currency': 'NGN', 
                'source_currency': 'NGN'
            }
        ).json()
        print(response_data)
        return response_data

    def load_bank_list(self):
        """
        Fetch bank details for all banks in Nigeria
        """

        url = 'https://api.flutterwave.com/v3/banks/NG'
        response_data = requests.get(url,
                                     headers={
                                         'Authorization': 'Bearer '+FLWSECK_TEST
                                     }
                                     )
        return response_data.json()['data']

    def account_number_verification(self, account_number, account_bank):
        """
        Verify if the account numbe submitted is valid
        """
        response = requests.post(
            'https://api.flutterwave.com/v3/accounts/resolve',
            headers={
                'Authorization': 'Bearer '+FLWSECK_TEST,
                'Accept': 'application/json'
            },
            json={
                "account_number": account_number,
                "account_bank": account_bank
            }
        ).json()
        return response

    def get_context_data(self, **kwargs):
        bank_list = self.load_bank_list()
        print(self.charge())
        # print(self.withdrawal_charge_fee())

        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['wallet_number'] = auth_wallet.number.hex
        context['bank_list'] = sorted(bank_list, key=lambda d: d['name'])
        return context

    def withdrawal_charge_fee(self):
        # url = 'https://api.flutterwave.com/v3/transfers/fee'
        # response_data = requests.get(url,
        #     headers={
        #         'Authorization': 'Bearer '+FLWSECK_TEST
        #     },
        #     json={
        #         "type": "account",
        #         "amount": 2700,
        #         "currency": "EUR"
        #     }
        # )
        res2 = rave.Transfer.getFee("EUR")
        print(res2)
        # print(response_data.json())
        # return response_data.json()

    def post(self,  request, *args, **kwargs):
        tx_ref = generateTransactionReference()
        account_bank = request.POST.get('account_bank')
        account_number = request.POST.get('account_number')
        amount = float(request.POST.get('amount'))
        narration = request.POST.get('narration')

        details = {
            "account_bank": account_bank,
            "account_number": account_number,
            "amount": amount,
            "narration": narration,
            "currency": "NGN",
            "reference": tx_ref,
            "callback_url": "https://webhook.site/b3e505b0-fe02-430e-a538-22bbbce8ce0d",
            "debit_currency": "NGN"
        }

        accountno_verify_res = self.account_number_verification(
            account_number, account_bank)
        if accountno_verify_res['status'] == 'error':
            return HttpResponse('Error')
        elif accountno_verify_res['status'] == 'success':
            details['beneficiary_name'] = accountno_verify_res['data']['account_name']
            rave = raveSetup()
            res = rave.Transfer.initiate(details)
            print(res)

            # To do:
            # if Transfer is successful (withdrawal)
            # TSave tp transaction history table
            # create a weebhook to track status,
            # Charge user account and move to pendingwithdrawal table
            # else
            # Prompt user


class TransactionView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/transaction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['wallet_number'] = auth_wallet.number.hex
        return context
