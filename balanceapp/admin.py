from django.contrib import admin
from .models import Bank, Transaction

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'balance', 'user')
    search_fields = ('bank_name', 'account_number', 'user__username')
    list_filter = ('user',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('bank', 'type', 'amount', 'date', 'description')
    search_fields = ('bank__bank_name', 'type', 'description')
    list_filter = ('type', 'date')
