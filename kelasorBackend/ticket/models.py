from django.db import models
from user.models import User
from bootcamp.models import Bootcamp

# Create your models here.
STATUS_CHOICES = (
        ('new', 'جدید'),
        ('in_progress', 'در حال بررسی'),
        ('answered', 'پاسخ داده شده'),
        ('closed', 'بسته شده'),
    )


class Ticket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255)
    bootcamp = models.ForeignKey(to=Bootcamp, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.user.phone}"
    

class TicketMessage(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='message')
    message = models.TextField()
    ticket_image = models.ImageField(upload_to='ticket_images', null=True, blank=True)
    ticket_file = models.FileField(upload_to='ticket_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TicketReply(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE) 
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پاسخ توسط {self.user.phone} در {self.ticket.subject}"