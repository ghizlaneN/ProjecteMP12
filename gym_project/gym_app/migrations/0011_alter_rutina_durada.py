# Generated by Django 4.2.11 on 2024-11-19 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0010_alter_rutina_durada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rutina',
            name='durada',
            field=models.CharField(choices=[('1', '1 hora'), ('2', '2 hores'), ('3', '3 hores'), ('4', '4 hores'), ('5', '5 hores')], default='1', max_length=5),
        ),
    ]
