# Generated by Django 4.1.1 on 2022-09-30 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ffl', '0007_team_defense_alter_player_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defense',
            name='fantasy_points',
            field=models.DecimalField(decimal_places=2, max_digits=13, verbose_name='Fantasy Points'),
        ),
    ]