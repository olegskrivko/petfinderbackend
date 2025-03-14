# Generated by Django 5.1.3 on 2024-11-24 21:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0010_remove_pet_event_occurred_at_alter_pet_author_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='identifier',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Vārds'),
        ),
        migrations.CreateModel(
            name='PetSightingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sightings', to='pets.pet')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_sightings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
