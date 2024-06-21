from django.db import models
from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE

# Create your models here.

#all transaction history stored on this database
class Trnasaction(models.Model):
    account = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name='transaction')
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)
    receiver_account_no = models.IntegerField(null=True, blank=True)
    timestamp  = models.DateTimeField(auto_now_add = True)
    loan_approve = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
