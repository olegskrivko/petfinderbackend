# Generated by Django 5.1.3 on 2025-04-03 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0022_alter_pet_pet_image_1_alter_pet_pet_image_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='pet_image_2',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='pet_image_3',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='pet_image_4',
        ),
    ]
