# Generated by Django 4.2.4 on 2023-08-15 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0008_masterstatus_date_masterstatus_note_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', models.CharField(max_length=254, verbose_name='phone')),
                ('service', models.CharField(choices=[('air transport', 'air transport'), ('transport', 'transport service'), ('warehouse', 'Warehouse service')], max_length=50, verbose_name='choose service')),
                ('massage', models.TextField(null=True, verbose_name='your quote massage')),
            ],
            options={
                'verbose_name': 'Quote',
                'verbose_name_plural': 'Quotes',
            },
        ),
    ]
