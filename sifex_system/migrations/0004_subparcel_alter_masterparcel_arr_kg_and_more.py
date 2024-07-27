# Generated by Django 4.2.4 on 2023-08-11 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0003_alter_masterparcel_date_received_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubParcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='masterparcel',
            name='arr_kg',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='masterparcel',
            name='arr_pcs',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='masterparcel',
            name='dlv_kg',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
