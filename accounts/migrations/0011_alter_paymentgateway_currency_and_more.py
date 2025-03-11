# Generated by Django 5.0.7 on 2025-03-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_paymentgateway_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentgateway',
            name='currency',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('USDT', 'Tether'), ('USDT', 'Ethereum')], max_length=10),
        ),
        migrations.AlterField(
            model_name='walletaddress',
            name='currency',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT', 'Tether'), ('USDT', 'Ethereum'), ('LTC', 'Litecoin'), ('TRX', 'Tron'), ('BCH', 'Bitcoin Cash')], max_length=10),
        ),
        migrations.AlterField(
            model_name='withdrawtransaction',
            name='currency',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT', 'Tether'), ('USDT', 'Ethereum'), ('LTC', 'Litecoin'), ('TRX', 'Tron'), ('BCH', 'Bitcoin Cash')], max_length=10),
        ),
    ]
