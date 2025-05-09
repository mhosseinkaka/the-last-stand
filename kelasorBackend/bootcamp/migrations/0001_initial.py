# Generated by Django 5.2 on 2025-04-28 20:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BootcampCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Bootcamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('capacity', models.PositiveIntegerField()),
                ('mentor_count', models.PositiveIntegerField(default=0)),
                ('teacher_count', models.PositiveIntegerField(default=0)),
                ('student_count', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('draft', 'پیش نویس'), ('open', 'درحال ثبت نام'), ('running', 'درحال برگزاری'), ('completed', 'برگزار شده'), ('cancelled', 'لغو شده')], default='draft', max_length=20)),
                ('location', models.CharField(default='Azadi Innovation Factory', max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='bootcamp')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('mentors', models.ManyToManyField(blank=True, related_name='mentor_bootcamp', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(blank=True, related_name='student_bootcamp', to=settings.AUTH_USER_MODEL)),
                ('teachers', models.ManyToManyField(blank=True, related_name='teacher_bootcamp', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bootcamp_category', to='bootcamp.bootcampcategory')),
            ],
        ),
    ]
