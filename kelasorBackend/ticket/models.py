from django.db import models
from user.models import User

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
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.user.phone}"
    

class TicketReply(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE) 
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پاسخ توسط {self.user.phone} در {self.ticket.subject}"