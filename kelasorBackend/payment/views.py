from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from user.permissions import IsSupportUser
from rest_framework.response import Response    
from payment.models import Payment, Installment
from payment.serializers import PaymentSerializer, InstallmentSerializer
from bootcamp.models import Bootcamp
from datetime import timedelta, date, timezone
# Create your views here.

class CreatePaymentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        bootcamp_id = self.kwargs.get('bootcamp_id')
        method = request.data.get('method')
        amount = request.data.get('amount')

        try:
            bootcamp = Bootcamp.objects.get(id=bootcamp_id)
        except Bootcamp.DoesNotExist:
            return Response({"detail": "بوتکمپ یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(
            user=request.user,
            bootcamp=bootcamp,
            amount=amount,
            method=method,
            tracking_number = request.data.get('tracking_number'),
            status='paid' if method == 'cash' else 'unpaid'
        )

        if method == 'installment':
            installment_amount = int(int(amount) / 4)
            today = date.today()
            for i in range(4):
                due_date = today + timedelta(days=30*i)  
                Installment.objects.create(
                    payment=payment,
                    amount=installment_amount,
                    due_date=due_date
                )

        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConfirmInstallmentPaymentView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsSupportUser]
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    
    def update(self, request, *args, **kwargs):
        installment = self.get_object()
        tracking_code = request.data.get("tracking_code")

        if installment.paid:
            return Response({"detail": "این قسط قبلاً پرداخت شده است."}, status=status.HTTP_400_BAD_REQUEST)

        installment.paid = True
        installment.paid_at = timezone.now()
        installment.tracking_code = tracking_code
        installment.save()

       
        all_paid = all(i.paid for i in installment.payment.installments.all())
        if all_paid:
            installment.payment.status = 'paid'
            installment.payment.save()

        return Response({"detail": "قسط با موفقیت تایید شد."}, status=status.HTTP_200_OK)
    

class PaymentSearchListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'method', 'bootcamp']
    search_fields = ['user_phone', 'bootcamp_title']
    ordering_fields = ['created_at', 'amount'] 
    ordering = ['-created_at']