# Generated by Django 5.0.1 on 2024-01-31 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organize_your_pet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='gender',
            field=models.CharField(choices=[('male', 'Samiec'), ('female', 'Samica')], default='male', max_length=10),
        ),
        migrations.AlterField(
            model_name='pet',
            name='species',
            field=models.CharField(choices=[('dog', 'Pies'), ('cat', 'Kot'), ('parrot', 'Papuga'), ('ferret', 'Fretka'), ('rabbit', 'Królik'), ('rodent', 'Gryzoń'), ('other', 'Inny')], default='other', max_length=50),
        ),
    ]
