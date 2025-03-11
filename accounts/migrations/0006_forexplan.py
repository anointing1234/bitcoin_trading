# Generated by Django 5.0.7 on 2025-03-09 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_account_country_alter_account_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForexPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('percentage', models.IntegerField(choices=[(5, '5%'), (69, '69%'), (120, '120%'), (200, '200%')])),
                ('duration', models.CharField(choices=[('After 6 Hours', 'After 6 Hours'), ('Hourly', 'Hourly'), ('Daily', 'Daily'), ('For 8 Hours', 'For 8 Hours'), ('Weekly', 'Weekly'), ('After 3 Months', 'After 3 Months'), ('After 6 Months', 'After 6 Months'), ('Forever', 'Forever')], max_length=20)),
                ('min_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('terms', models.CharField(max_length=100)),
                ('purchase_url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
