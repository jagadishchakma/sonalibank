from django.contrib import admin
from .models import Trnasaction
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
# Register your models here.
def send_transaction_email(self, msg, amount, type):
        mail_subject=msg
        message = render_to_string('deposit_email.html', {'user':{'first_name':self.account.user.first_name, 'last_name':self.account.user.last_name}, 'amount':amount, 'type': type})
        to_email = self.account.user.email
        send_email = EmailMultiAlternatives(mail_subject,'',to=[to_email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()
@admin.register(Trnasaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account','amount','balance_after_transaction','transaction_type','loan_approve']
    def save_model(self,request,obj,form,change):
        obj.account.balance += obj.amount
        obj.balance_after_transaction = obj.account.balance
        obj.account.save()
        send_transaction_email(obj, 'loan approved message', obj.amount, 'loan approved')
        super().save_model(request,obj,form,change)