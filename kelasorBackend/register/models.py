from django.db import models
from user.models import User
from bootcamp.models import Bootcamp

# Create your models here.

STATUS_CHOICES = (
        ('pending', 'در حال انتظار'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
        ('cancelled', 'کنسل شده'),
    )

class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='register_student')
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name='register_bootcamp')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'bootcamp')  

    def __str__(self):
        return f"{self.student.phone} -> {self.bootcamp.title} ({self.status})"