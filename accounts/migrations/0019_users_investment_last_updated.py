# Generated by Django 5.0.7 on 2025-03-18 15:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_tingatingaplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='users_investment',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
