# Generated by Django 4.2.4 on 2023-09-06 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0018_alter_masterawb_arr_kg_alter_masterawb_dlv_kg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterawb',
            name='number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='masterawb',
            name='number_of_parcel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='masterawb',
            name='parcel_kg',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='slaveawb',
            name='number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='masterawb',
            name='awb_type',
            field=models.CharField(choices=[('normal awb', 'Normal awb'), ('express awb', 'Express awb'), ('shengzen awb', 'Shengzen awb')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='slaveawb',
            name='awb_type',
            field=models.CharField(choices=[('normal awb', 'Normal awb'), ('express awb', 'Express awb'), ('shengzen awb', 'Shengzen awb')], max_length=255, null=True),
        ),
    ]
