from django.contrib import admin
from payment.models import Payment, Installment
# Register your models here.
admin.site.register(Payment)    
admin.site.register(Installment)