# Generated by Django 5.2 on 2025-05-06 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootcamp', '0001_initial'),
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='bootcamp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bootcamp.bootcamp'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_file',
            field=models.FileField(blank=True, null=True, upload_to='ticket_files'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_image',
            field=models.ImageField(blank=True, null=True, upload_to='ticket_images'),
        ),
    ]
