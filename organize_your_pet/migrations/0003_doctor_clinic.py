# Generated by Django 5.0.1 on 2024-01-31 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organize_your_pet', '0002_alter_pet_gender_alter_pet_species'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organize_your_pet.clinic'),
        ),
    ]