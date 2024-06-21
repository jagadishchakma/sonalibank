from django.urls import path
from . import views
urlpatterns = [
    path('deposit/', views.DepositMoneyView.as_view(), name='deposit_money'),
    path('report/', views.TransactionReportView.as_view(), name='transaction_report'),
    path('withdraw/', views.WithdrawMoneyView.as_view(), name='withdraw_money'),
    path('loanrequest/', views.LoanRequestView.as_view(), name='loan_request'),
    path('loans/', views.LoanListView.as_view(), name='loan_list'),
    path('loan/<int:loan_id>/', views.PayLoanView.as_view(), name='loan_pay'),
    path('transfer/', views.BalanceTransferView.as_view(), name='balance_transfer'),
]
