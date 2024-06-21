from datetime import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Trnasaction
from .forms import DepositForm,WithdrawalForm,LoanRequestForm, BalanceTransferForm
from .constants import Deposit,Withdrawal,Loan_Paid,Loan, Balance_Transfer
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse_lazy
from accounts.models import UserBankAccount
from core.models import SiteAdmin
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name  = 'transaction_form.html'
    model = Trnasaction
    title = ''
    success_url = reverse_lazy('transaction_report')


    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account
        })
        return kwargs
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context
    def send_transaction_email(self, msg, amount, type):
        mail_subject=msg
        message = render_to_string('deposit_email.html', {'user':self.request.user, 'amount':amount, 'type': type})
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject,'',to=[to_email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposite Page'


    def get_initial(self):
        initial = {'transaction_type': Deposit}
        return initial  
    def form_valid(self,form):
        amount = form.cleaned_data['amount']
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )

        messages.success(self.request, f"{amount}$ was deposited to your account successfully.")
        self.send_transaction_email('deposit message', amount, 'deposit')
        return super().form_valid(form)
    
    
class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawalForm 
    title = 'Withdraw Money Page'

    def get_initial(self):
        initial = {'transaction_type': Withdrawal}
        return initial  
    def form_valid(self,form):
        last_decision = SiteAdmin.objects.latest('created_at')
        decision = last_decision.bankrupt
        if decision is not True:
            amount = form.cleaned_data['amount']
            account = self.request.user.account
            account.balance -= amount
            account.save(
                update_fields = ['balance']
            )

            messages.success(self.request, f"Successfully withdrawn {amount}$ to your account.")
            super().send_transaction_email('withdraw message', amount, 'withdraw')
        else:
             messages.warning(self.request, f"Sorry, Bank is now bankruft. You can't withdraw now.")
        return super().form_valid(form)


class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm 
    title = 'Loan Request Page'

    def get_initial(self):
        initial = {'transaction_type': Loan}
        return initial  
    def form_valid(self,form):
        amount = form.cleaned_data['amount']
        current_loan_count = Trnasaction.objects.filter(account = self.request.user.account, transaction_type=3, loan_approve = True).count()
        if current_loan_count >= 3:
            return HttpResponse('You have crossed your loan limits')
        # account = self.request.user.account
        # account.balance -= amount
        # account.save(
        #     update_fields = ['balance']
        # )

        messages.success(self.request, f"Successfully withdrawn {amount}$ to your account.")
        super().send_transaction_email('loan request message', amount, 'loan request')
        return super().form_valid(form)


class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transaction_report.html'
    model = Trnasaction
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance  = Trnasaction.objects.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
        return queryset
        
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })
        return context
       


class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Trnasaction, id=loan_id)
        if loan.loan_approve:
            user_account = loan.account
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.transaction_type = Loan_Paid
                loan.save()
                return redirect('loan_list')
            else:
                messages.error(self.request, f'loan amount is greater than available balance') 
                redirect('loan_list')


class LoanListView(LoginRequiredMixin, ListView):
    model = Trnasaction
    template_name = 'loan_request.html'
    context_object_name = 'loans'

    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Trnasaction.objects.filter(account = user_account, transaction_type=Loan)
        return queryset


class BalanceTransferView(TransactionCreateMixin):
    form_class = BalanceTransferForm 
    title = 'Balance Transfer'

    def get_initial(self):
        initial = {'transaction_type': Balance_Transfer}
        return initial  
    def form_valid(self,form):
        amount = form.cleaned_data['amount']
        account = self.request.user.account
        account.balance -= amount
        account.save(
            update_fields = ['balance']
        )
        receiver_account = UserBankAccount.objects.get(account_no=form.cleaned_data['receiver_account_no'])
        receiver_account.balance += amount

        messages.success(self.request, f"{amount}$ was transfered to this account {receiver_account.account_no} successfully.")
        super().send_transaction_email('Balance Transfer message', amount, 'Balance Transfer')
        return super().form_valid(form)


