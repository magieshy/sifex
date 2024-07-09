# Generated by Django 4.2.4 on 2023-09-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0014_slaveawb_slavestatus_remove_substatus_sub_parcel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterawb',
            name='awb_type',
            field=models.CharField(choices=[('normal goods', 'Normal goods'), ('express goods', 'Express goods'), ('shengzen goods', 'Shengzen goods')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='slaveawb',
            name='awb_type',
            field=models.CharField(choices=[('normal goods', 'Normal goods'), ('express goods', 'Express goods'), ('shengzen goods', 'Shengzen goods')], max_length=255, null=True),
        ),
    ]
