# Generated by Django 4.2.4 on 2024-07-15 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0046_masterawb_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterawb',
            name='receiver_company',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='masterawb',
            name='sender_company',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
