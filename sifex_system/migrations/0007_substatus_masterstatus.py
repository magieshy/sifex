# Generated by Django 4.2.4 on 2023-08-15 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0006_subparcel_awb_subparcel_order_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_parcel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sifex_system.subparcel')),
            ],
        ),
        migrations.CreateModel(
            name='MasterStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sifex_system.masterparcel')),
            ],
        ),
    ]
