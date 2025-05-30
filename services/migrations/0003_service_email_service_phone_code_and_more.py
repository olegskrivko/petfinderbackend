# Generated by Django 5.1.3 on 2025-04-18 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_remove_location_address_remove_location_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-pasts'),
        ),
        migrations.AddField(
            model_name='service',
            name='phone_code',
            field=models.CharField(blank=True, choices=[('+371', 'Latvija (+371)'), ('+370', 'Lietuva (+370)'), ('+372', 'Igaunija (+372)')], max_length=5, null=True, verbose_name='Telefona kods'),
        ),
        migrations.AddField(
            model_name='service',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefona numurs'),
        ),
    ]
