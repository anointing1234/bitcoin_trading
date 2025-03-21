# Generated by Django 5.0.7 on 2025-03-18 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_withdrawtransaction_withdraw_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='TingaTingaPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('percentage', models.IntegerField(choices=[(5, '5% Daily'), (10, '10% Daily'), (15, '15% Daily'), (20, '20% Daily')], help_text='Daily profit percentage')),
                ('min_amount', models.DecimalField(decimal_places=2, help_text='Minimum investment amount', max_digits=10)),
                ('max_amount', models.DecimalField(decimal_places=2, help_text='Maximum investment amount', max_digits=10)),
                ('duration_days', models.IntegerField(help_text='Duration of the plan in days')),
            ],
        ),
    ]
