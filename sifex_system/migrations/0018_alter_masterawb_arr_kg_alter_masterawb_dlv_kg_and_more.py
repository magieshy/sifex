# Generated by Django 4.2.4 on 2023-09-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0017_slaveawb_accepted_slaveawb_arrived_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterawb',
            name='arr_kg',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='masterawb',
            name='dlv_kg',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='slaveawb',
            name='arr_kg',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='slaveawb',
            name='awb_kg',
            field=models.FloatField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='slaveawb',
            name='dlv_kg',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
    ]
