from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from .models import Payment, Installment

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