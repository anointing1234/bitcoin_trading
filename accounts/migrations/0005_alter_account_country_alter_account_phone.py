# Generated by Django 5.0.7 on 2025-03-08 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_balance_usdt_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='country',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
