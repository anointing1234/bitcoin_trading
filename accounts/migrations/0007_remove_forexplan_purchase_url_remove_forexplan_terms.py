# Generated by Django 5.0.7 on 2025-03-09 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_forexplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forexplan',
            name='purchase_url',
        ),
        migrations.RemoveField(
            model_name='forexplan',
            name='terms',
        ),
    ]
