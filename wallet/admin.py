from django.contrib import admin

from wallet.models import TransactionHistory, Wallet

# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    readonly_fields = ('number', )
admin.site.register(Wallet, WalletAdmin)

admin.site.register(TransactionHistory)