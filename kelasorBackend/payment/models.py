from django.db import models
from user.models import User
from bootcamp.models import Bootcamp
# Create your models here.

PAYMENT_METHODS = (
        ('cash', 'نقدی'),
        ('installment', 'قسطی'))

STATUS_CHOICES = (
        ('unpaid', 'پرداخت نشده'),
        ('paid', 'پرداخت شده'))


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    tracking_number = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} - {self.bootcamp.title} ({self.method})"


class Installment(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='installments_payment')
    amount = models.PositiveIntegerField()
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    warranty_check = models.FileField(upload_to="warranty_check", null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    tracking_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"قسط {self.id} - {self.payment.user.phone}"
    

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"فاکتور {self.user.phone} - مبلغ {self.amount}"