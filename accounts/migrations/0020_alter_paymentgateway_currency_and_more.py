# Generated by Django 5.0.7 on 2025-03-18 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_users_investment_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentgateway',
            name='currency',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('USDT_TRC20', 'Tether (USDT - TRC20)'), ('USDT_ERC20', 'Tether (USDT - ERC20)')], max_length=15),
        ),
        migrations.AlterField(
            model_name='walletaddress',
            name='currency',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT_TRC20', 'Tether (USDT - TRC20)'), ('USDT_ERC20', 'Tether (USDT - ERC20)'), ('LTC', 'Litecoin'), ('TRX', 'Tron'), ('BCH', 'Bitcoin Cash')], max_length=15),
        ),
        migrations.AlterField(
            model_name='withdrawtransaction',
            name='currency',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('USDT_TRC20', 'Tether (USDT - TRC20)'), ('USDT_ERC20', 'Tether (USDT - ERC20)'), ('LTC', 'Litecoin'), ('TRX', 'Tron'), ('BCH', 'Bitcoin Cash')], max_length=15),
        ),
    ]
