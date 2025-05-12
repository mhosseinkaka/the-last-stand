from django.urls import path
from payment.views import CreatePaymentView, ConfirmInstallmentPaymentView, PaymentSearchListView, MyPaymentsView, CreateInvoiceView

urlpatterns = [
    path('bootcamp/<int:bootcamp_id>/pay/', CreatePaymentView.as_view(), name='create-payment'),
    path('installment/<int:pk>/confirm/', ConfirmInstallmentPaymentView.as_view(), name='confirm-installment'),
    path('search/', PaymentSearchListView.as_view(), name='payment-search'),
    path('myPayments/', MyPaymentsView.as_view(), name='my-payments'),
    path('invoice-create/', CreateInvoiceView.as_view(), name='invoice-create'),
]