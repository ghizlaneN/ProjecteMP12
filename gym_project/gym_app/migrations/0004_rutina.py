# Generated by Django 4.2.11 on 2024-11-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0003_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rutina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('descripcio', models.TextField()),
                ('exercicis', models.TextField()),
                ('durada', models.IntegerField()),
                ('recomenacions', models.TextField()),
                ('horari', models.CharField(max_length=50)),
            ],
        ),
    ]
