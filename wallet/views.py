from decimal import Decimal
import json
from django import template
from django.http import HttpResponse, request
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Sum

import rave_python.rave_exceptions as RaveExceptions
from ewallet.utils import generateTransactionReference, raveSetup, FLWSECK_TEST, REDIRECT_DOMAIN

import requests
from django.shortcuts import redirect, render
from django.contrib import messages
from django.template.loader import render_to_string

from wallet.models import TransactionHistory, Wallet, PendingWithdrawal

from user.mixins import VerificationRequiredMixin


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
class RecordPendingWithdrawal:
    def __init__(self, reference, user, amount):
        self.reference = reference
        self.user = user
        self.amount = amount

    def save(self):
        PendingWithdrawal.objects.create(
            reference=self.reference,
            user=self.user,
            amount=self.amount
        )


class WalletView(LoginRequiredMixin, VerificationRequiredMixin, TemplateView):
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
        amount_funded = TransactionHistory.objects.filter(
            by=auth, success=True, type='FW').aggregate(total_amount_funded=Sum('amount'))
        transactions = (TransactionHistory.objects.filter(
            by=auth, success=True).order_by('-date')[:5])

        context['transactions'] = transactions
        context['amount_sent'] = amount_sent['total_amount_sent'] if amount_sent['total_amount_sent'] else 0
        context['amount_received'] = amount_received['total_amount_received'] if amount_received['total_amount_received'] else 0
        context['amount_funded'] = amount_funded['total_amount_funded'] if amount_funded['total_amount_funded'] else 0
        context['transaction_times'] = transaction_times
        context['balance'] = auth_wallet.balance
        context['wallet_number'] = auth_wallet.number.hex

        return context


class SendFundView(LoginRequiredMixin, VerificationRequiredMixin, TemplateView):
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
        context['balance'] = auth_wallet.balance
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
                auth_wallet = Wallet.objects.filter(user=auth).first()
                context = {
                    'error_msg': 'Enter positive amount',
                    'balance': auth_wallet.balance,
                    'wallet_number': auth_wallet.number.hex
                }
                rendered = render_to_string(
                    'html/wallet/failed-fund.html', context=context)
                return HttpResponse(rendered)

            else:
                auth_wallet = Wallet.objects.filter(user=auth).first()
                context = {
                    'error_msg': 'Insufficient Fund',
                    'balance': auth_wallet.balance,
                    'wallet_number': auth_wallet.number.hex
                }
                rendered = render_to_string(
                    'html/wallet/failed-fund.html', context=context)
                return HttpResponse(rendered)

        except ValidationError:
            return HttpResponse('Wallet Does Not exist')

        auth_wallet = Wallet.objects.filter(user=auth).first()
        context = {
            'error_msg': 'Deposit succcessful',
            'balance': auth_wallet.balance,
            'wallet_number': auth_wallet.number.hex
        }
        rendered = render_to_string(
            'html/wallet/successful-transfer.html', context=context)
        return HttpResponse(rendered)


class ReceiveFundView(LoginRequiredMixin, VerificationRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/receive-fund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['balance'] = auth_wallet.balance
        context['wallet_number'] = auth_wallet.number.hex
        return context


class FundWalletProccessView(LoginRequiredMixin, VerificationRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/successful-fund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['balance'] = auth_wallet.balance
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


class FundWalletView(LoginRequiredMixin, VerificationRequiredMixin, TemplateView):
    """
    Fund the user wallet
    """
    login_url = '/login/'
    template_name = 'html/wallet/fund-wallet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['balance'] = auth_wallet.balance
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
            'redirect_url': REDIRECT_DOMAIN+"/wallet/fund-wallet/success",
            'customer': {
                'email': request.user.email,
                'name': request.user.name,
            }
        }
        response_data = requests.post(
            "https://api.flutterwave.com/v3/payments",
            headers={'Authorization': 'Bearer '+FLWSECK_TEST},
            json=json
        )
        response_data = response_data.json()
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

        auth_wallet = Wallet.objects.filter(user=auth).first()
        context = {
            'error_msg': 'Unable to fund wallet',
            'balance': auth_wallet.balance,
            'wallet_number': auth_wallet.number.hex
        }
        rendered = render_to_string(
            'html/wallet/failed-fund.html', context=context)
        return HttpResponse(rendered)

class WithdrawWalletView(LoginRequiredMixin, VerificationRequiredMixin, TemplateView):
    """
    Withdraw from user wallet to any bank account
    """
    login_url = '/login/'
    template_name = 'html/wallet/withdraw-wallet.html'

    def load_bank_list(self):
        """
        Fetch bank details for all banks in Nigeria
        """
        url = 'https://api.flutterwave.com/v3/banks/NG'
        response_data = requests.get(
            url,
            headers = {
                'Authorization': 'Bearer '+FLWSECK_TEST
            }
        )
        return response_data.json()['data']

    def account_number_verification(self, account_number, account_bank):
        """
        Verify if the account numbe submitted is valid
        """

        url = "https://api.flutterwave.com/v3/accounts/resolve"
        headers = {
            "Authorization": "Bearer "+FLWSECK_TEST,
            "Content-Type": "application/json"
        }
        data = {
            "account_number": account_number,
            "account_bank": account_bank
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def get_context_data(self, **kwargs):
        bank_list = self.load_bank_list()

        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['balance'] = auth_wallet.balance
        context['wallet_number'] = auth_wallet.number.hex
        context['bank_list'] = sorted(bank_list, key=lambda d: d['name'])
        return context

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
            # "callback_url": "https://webhook.site/b3e505b0-fe02-430e-a538-22bbbce8ce0d",
            "callback_url": REDIRECT_DOMAIN+"/wallet/withdraw-wallet/status/",
            "debit_currency": "NGN"
        }

        accountno_verify_res = self.account_number_verification(
            account_number, account_bank)
        if accountno_verify_res['status'] == 'error':
            return HttpResponse('Unable to verify account number')
        elif accountno_verify_res['status'] == 'success':
            details['beneficiary_name'] = accountno_verify_res['data']['account_name']
            # res = rave.Transfer.initiate(details)
            url = "https://api.flutterwave.com/v3/transfers"
            headers = {
                "Authorization": "Bearer "+FLWSECK_TEST,
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=details).json()
            # if transfer is successful and queued (withdrawal)
            if response['status'] == 'success':
                auth = self.request.user
                auth_wallet = Wallet.objects.filter(user=auth).first()
                # If amount to withdraw is greater than balance
                if amount > auth_wallet.balance:
                    return HttpResponse('Insufficient balance')
                auth_wallet.balance -= amount
                auth_wallet.save()
                record_pending_withdrawal = RecordPendingWithdrawal(
                    reference=tx_ref,
                    user=auth,
                    amount=amount,
                )
                record_pending_withdrawal.save()
                # Save to transaction history table
                record_transaction = RecordTransactionHistory(
                    reference=tx_ref,
                    amount=amount,
                    details='Withdrawal',
                    type='WW', 
                    success=False,
                    by=auth,
                    to=auth
                )
                record_transaction.save()
                return HttpResponse('Withdrawal successful')
            else:
                return HttpResponse('Unable to withdraw')


class TransactionView(LoginRequiredMixin, VerificationRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'html/wallet/transaction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user
        auth_wallet = Wallet.objects.filter(user=auth).first()
        context['balance'] = auth_wallet.balance
        context['wallet_number'] = auth_wallet.number.hex
        return context

def withdraw_wallet_status(request):
    """
    This function is called by flutterwave after a withdrawal is made, and the transaaction either fails or succeeds
    """
    if request.method == 'GET':
        response_data = request.body.decode('utf-8')
        response_data = json.loads(response_data)
        # print(response_data)
        if response_data['status'] == 'SUCCESSFUL':
            # update pending withdrawal
            pending_withdrawal = PendingWithdrawal.objects.filter(
                reference=response_data['data']['reference']).first()
            pending_withdrawal.status = 'SUCCESS'
            pending_withdrawal.save()
            # update transaction history
            transaction_history = RecordTransactionHistory.objects.filter(
                reference=response_data['data']['reference']).first()
            transaction_history.success = True
            transaction_history.save()
            return HttpResponse('success')
        elif response_data['status'] == 'FAILED':
            # update pending withdrawal
            pending_withdrawal = PendingWithdrawal.objects.filter(
                reference=response_data['data']['reference']).first()
            pending_withdrawal.status = 'FAILED'
            pending_withdrawal.save()
            # update transaction history
            transaction_history = RecordTransactionHistory.objects.filter(
                reference=response_data['data']['reference']).first()
            transaction_history.success = False
            transaction_history.save()
            # update wallet balance
            auth = pending_withdrawal.user
            auth_wallet = Wallet.objects.filter(user=auth).first()
            auth_wallet.balance += pending_withdrawal.amount
            return HttpResponse('failed')
    else:
        return HttpResponse('Invalid request')