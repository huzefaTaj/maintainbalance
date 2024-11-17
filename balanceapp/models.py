from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate bank with a user
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, unique=True, blank=True,null=True )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type.capitalize()} - ${self.amount} on {self.date.strftime('%Y-%m-%d')}"
    
class SpendingLimit(models.Model):
    """
    Model to store a daily spending limit for users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="spending_limit")
    limit = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('500.00'))

    def __str__(self):
        return f"{self.user.username} - Limit: {self.limit}"
