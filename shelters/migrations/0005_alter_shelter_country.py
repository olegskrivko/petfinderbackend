# Generated by Django 5.1.3 on 2024-12-07 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelters', '0004_shelter_social_media_alter_shelter_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelter',
            name='country',
            field=models.CharField(default=1, max_length=100, verbose_name='Valsts'),
            preserve_default=False,
        ),
    ]
