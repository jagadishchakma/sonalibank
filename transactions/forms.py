from django import forms 
from .models import Trnasaction
from accounts.models import UserBankAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Trnasaction
        fields = ['amount', 'transaction_type']
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args,**kwargs)

        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()
    

    def save(self):
        self.instance.account = self.account #self.instance.account vaiable e == current user er bank account set kore dilam but naaa dileo direct kora jeto
        self.instance.balance_after_transaction = self.account.balance
        return super().save()

class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(f"You need to deposit at least; {min_deposit_amount}$")
        return amount

class WithdrawalForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(f"You can withdraw at least {min_withdraw_amount} $")
        if amount > max_withdraw_amount:
            raise forms.ValidationError(f"You can withdraw at most {max_withdraw_amount} $")
        
        if amount > balance:
            raise forms.ValidationError(f'You have {balance}$ in your account. You can not winthdraw more than your account balance.')
        return amount

class  LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount


class BalanceTransferForm(TransactionForm):
    class Meta:
        model = Trnasaction
        fields = ['amount', 'receiver_account_no','transaction_type']
    def clean_amount(self):
        account = self.account
        min_transfer_amount = 1000
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount > balance:
            raise forms.ValidationError(f"Your balance is insufficient")
        if amount < min_transfer_amount:
            raise forms.ValidationError(f"You can transfer at at least {min_transfer_amount} $")
        return amount
    
    def clean_receiver_account_no(self):
        receiver_account_no = self.cleaned_data.get('receiver_account_no')
        try:
            UserBankAccount.objects.get(account_no = receiver_account_no)
            return receiver_account_no
        except:
            raise forms.ValidationError(f"Receiver Account Does Not Exist")
       
        
