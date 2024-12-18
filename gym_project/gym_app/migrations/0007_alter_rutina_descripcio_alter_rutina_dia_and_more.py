# Generated by Django 4.2.11 on 2024-11-12 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0006_remove_rutina_horari_rutina_hora_alter_rutina_dia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rutina',
            name='descripcio',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='rutina',
            name='dia',
            field=models.CharField(choices=[('dilluns', 'Dilluns'), ('dimarts', 'Dimarts'), ('dimecres', 'Dimecres'), ('dijous', 'Dijous'), ('divendres', 'Divendres')], default='Dilluns', max_length=10),
        ),
        migrations.AlterField(
            model_name='rutina',
            name='durada',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='1', max_length=5),
        ),
        migrations.AlterField(
            model_name='rutina',
            name='hora',
            field=models.CharField(choices=[('16:00', '16:00 '), ('17:00', '17:00 '), ('18:00', '18:00 '), ('19:00', '19:00 '), ('20:00', '20:00 ')], default="'16:00", max_length=5),
        ),
    ]
