# Generated by Django 4.2.4 on 2023-09-20 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0032_remove_lineitem_amount_lineitem_amount_tz_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='total_amount_tz',
            new_name='total_amount_tzs',
        ),
    ]
