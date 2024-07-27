# Generated by Django 4.2.4 on 2024-07-27 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0059_masterawb_bay_masterawb_rack'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='masterawb',
            name='bay',
        ),
        migrations.RemoveField(
            model_name='masterawb',
            name='rack',
        ),
        migrations.CreateModel(
            name='AwbLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rack', models.CharField(blank=True, max_length=255, null=True)),
                ('bay', models.CharField(blank=True, max_length=255, null=True)),
                ('pcs', models.CharField(blank=True, max_length=255, null=True)),
                ('awb', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='awb_locations', to='sifex_system.masterawb')),
            ],
        ),
    ]
