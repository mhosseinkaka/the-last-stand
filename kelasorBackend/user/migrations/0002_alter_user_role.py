# Generated by Django 5.2 on 2025-04-26 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('support1', 'Support1'), ('support2', 'Support2'), ('support3', 'Support3'), ('superuser', 'Superuser'), ('teacher', 'Teacher')], default='student'),
        ),
    ]
