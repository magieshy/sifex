# Generated by Django 4.2.4 on 2024-07-26 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0055_alter_invoice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterawb',
            name='invoice_generated',
            field=models.BooleanField(default=False),
        ),
    ]
