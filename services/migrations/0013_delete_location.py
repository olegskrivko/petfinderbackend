# Generated by Django 5.1.3 on 2025-05-03 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_service_service_image_delete_workinghour'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
    ]
