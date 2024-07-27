# Generated by Django 4.2.4 on 2023-08-23 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sifex_system', '0009_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterparcel',
            name='accepted',
            field=models.BooleanField(default=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='masterstatus',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master_status', to='sifex_system.masterparcel'),
        ),
        migrations.AlterField(
            model_name='masterstatus',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'accepted'), ('LOADED', 'loaded'), ('MANIFATED', 'manifested'), ('RCS - recieved from shipper', 'RCS recieved from shipper'), ('OFFLOADED', 'offloaded'), ('DEPARTED', 'departed'), ('ON TRANSIT', 'on transit'), ('ARRIVED', 'arrived'), ('UNDER CLEARANCE', 'under clearance'), ('DELIVERED', 'derivered')], max_length=50, null=True, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='substatus',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'accepted'), ('LOADED', 'loaded'), ('MANIFATED', 'manifested'), ('RCS - recieved from shipper', 'RCS recieved from shipper'), ('OFFLOADED', 'offloaded'), ('DEPARTED', 'departed'), ('ON TRANSIT', 'on transit'), ('ARRIVED', 'arrived'), ('UNDER CLEARANCE', 'under clearance'), ('DELIVERED', 'derivered')], max_length=50, null=True, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='substatus',
            name='sub_parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_status', to='sifex_system.subparcel'),
        ),
    ]
