# Generated by Django 4.1.3 on 2022-11-02 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ffl', '0002_remove_pick_defense_id_remove_pick_defense_points_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defense',
            name='fantasy_points',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=13, verbose_name='Fantasy Points'),
        ),
        migrations.AlterField(
            model_name='pick',
            name='defense',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='defense', to='ffl.defense'),
        ),
    ]