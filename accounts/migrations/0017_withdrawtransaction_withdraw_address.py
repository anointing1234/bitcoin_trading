# Generated by Django 5.0.7 on 2025-03-11 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_balance_total_profits'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawtransaction',
            name='withdraw_address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
