from django.urls import path
from payment.views import CreatePaymentView, ConfirmInstallmentPaymentView, PaymentSearchListView

urlpatterns = [
    path('bootcamp/<int:bootcamp_id>/pay/', CreatePaymentView.as_view(), name='create-payment'),
    path('installment/<int:pk>/confirm/', ConfirmInstallmentPaymentView.as_view(), name='confirm-installment'),
    path('search/', PaymentSearchListView.as_view(), name='payment-search'),
]