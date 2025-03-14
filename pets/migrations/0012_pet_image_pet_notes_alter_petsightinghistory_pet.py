# Generated by Django 5.1.3 on 2024-11-24 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0011_alter_pet_identifier_alter_pet_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pet_images/', verbose_name='Attēls'),
        ),
        migrations.AddField(
            model_name='pet',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Piezīmes'),
        ),
        migrations.AlterField(
            model_name='petsightinghistory',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sightings_history', to='pets.pet'),
        ),
    ]
