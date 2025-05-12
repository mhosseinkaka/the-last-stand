from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from payment.models import Payment, Installment, Invoice

class InstallmentSerializer(ModelSerializer):
    class Meta:
        model = Installment
        fields = '__all__'

class PaymentSerializer(ModelSerializer):
    installments = InstallmentSerializer(many=True, read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    bootcamp_title = serializers.CharField(source='bootcamp.title', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentListSerializer(ModelSerializer):
    installments = InstallmentSerializer(many=True, read_only=True)
    bootcamp_title = serializers.CharField(source='bootcamp.title', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'method', 'status', 'created_at', 'bootcamp_title', 'installments']


class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'user', 'bootcamp', 'amount', 'description', 'created_by', 'created_at', 'paid']
        read_only_fields = ['created_by', 'created_at', 'paid']