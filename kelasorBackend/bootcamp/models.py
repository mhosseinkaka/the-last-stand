from django.db import models
from user.models import User
# Create your models here.

STATUS_CHOICES = (
        ('draft', 'پیش نویس'),
        ('open', 'درحال ثبت نام'),
        ('running', 'درحال برگزاری'),
        ('completed', 'برگزار شده'),
        ('cancelled', 'لغو شده'))

class BootcampCategory(models.Model):
    name = models.CharField(max_length = 250)
    
    def __str__(self):
        return self.name
    
class Bootcamp(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(BootcampCategory, on_delete=models.CASCADE, null=True, related_name='bootcamp_category')
    price = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.PositiveIntegerField()
    mentor_count = models.PositiveIntegerField(default=0)
    teacher_count = models.PositiveIntegerField(default=0)
    student_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    location = models.CharField(max_length=100, default='Azadi Innovation Factory')
    file = models.FileField(upload_to="bootcamp", null=True, blank=True)
    mentors = models.ManyToManyField(User, related_name='mentor_bootcamp', blank=True)
    teachers = models.ManyToManyField(User, related_name='teacher_bootcamp', blank=True)
    students = models.ManyToManyField(User, related_name='student_bootcamp', blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title