# Generated by Django 4.2.4 on 2023-09-02 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0016_alter_masterawb_awb_kg'),
    ]

    operations = [
        migrations.AddField(
            model_name='slaveawb',
            name='accepted',
            field=models.BooleanField(default=True, max_length=255),
        ),
        migrations.AddField(
            model_name='slaveawb',
            name='arrived',
            field=models.BooleanField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='slaveawb',
            name='delivered',
            field=models.BooleanField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='slaveawb',
            name='departed',
            field=models.BooleanField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='slaveawb',
            name='loaded',
            field=models.BooleanField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='slaveawb',
            name='manifested',
            field=models.BooleanField(default=False, max_length=255),
        ),
        migrations.AddField(
            model_name='slaveawb',
            name='under_clearance',
            field=models.BooleanField(default=False, max_length=255),
        ),
    ]
