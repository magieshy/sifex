# Generated by Django 4.2.4 on 2023-09-20 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0030_systempreference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='total_amount',
            new_name='total_amount_tz',
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_amount_usd',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]
