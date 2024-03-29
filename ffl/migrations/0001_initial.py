# Generated by Django 4.1.1 on 2022-10-13 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="FantasyTeam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="default name", max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=20,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="id",
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="Name")),
                (
                    "position",
                    models.CharField(default="", max_length=5, verbose_name="Position"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("team_id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "team_abbr",
                    models.CharField(
                        default="", max_length=5, verbose_name="Team Name Abbreviation"
                    ),
                ),
                (
                    "team_name",
                    models.CharField(
                        default="", max_length=30, verbose_name="Team Name"
                    ),
                ),
                (
                    "team_color",
                    models.CharField(
                        default="", max_length=10, verbose_name="Primary Color"
                    ),
                ),
                (
                    "team_color2",
                    models.CharField(
                        default="", max_length=10, verbose_name="Secondary Color"
                    ),
                ),
                (
                    "team_color3",
                    models.CharField(
                        default="", max_length=10, verbose_name="Tertiary Color"
                    ),
                ),
                (
                    "team_color4",
                    models.CharField(
                        default="", max_length=10, verbose_name="Quaternary Color"
                    ),
                ),
                (
                    "team_logo",
                    models.CharField(
                        default="", max_length=250, verbose_name="Team Logo"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayerWeek",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("season", models.IntegerField(default=2022, verbose_name="Season")),
                ("week", models.IntegerField(verbose_name="Week")),
                ("points", models.FloatField(default=0.0, verbose_name="Points")),
                (
                    "passing_yds",
                    models.IntegerField(default=0, verbose_name="Passing Yards"),
                ),
                (
                    "passing_tds",
                    models.IntegerField(default=0, verbose_name="Passing Touchdowns"),
                ),
                (
                    "passing_ints",
                    models.IntegerField(
                        default=0, verbose_name="Passing Interceptions"
                    ),
                ),
                (
                    "rushing_yds",
                    models.IntegerField(default=0, verbose_name="Rushing Yards"),
                ),
                (
                    "rushing_tds",
                    models.IntegerField(default=0, verbose_name="Rushing Touchdowns"),
                ),
                (
                    "receiving_yds",
                    models.IntegerField(default=0, verbose_name="Receiving Yards"),
                ),
                (
                    "receiving_tds",
                    models.IntegerField(default=0, verbose_name="Receiving Touchdowns"),
                ),
                (
                    "kick_ret_tds",
                    models.IntegerField(
                        default=0, verbose_name="Kick Return Touchdowns"
                    ),
                ),
                (
                    "two_point_conversions",
                    models.IntegerField(
                        default=0, verbose_name="Two Point Conversions"
                    ),
                ),
                (
                    "fumbles_lost",
                    models.IntegerField(default=0, verbose_name="Fumbles Lost"),
                ),
                (
                    "fumbles_rec_tds",
                    models.IntegerField(
                        default=0, verbose_name="Fumble Recovery Touchdowns"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weeks",
                        to="ffl.player",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="player",
            name="team",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="players",
                to="ffl.team",
            ),
        ),
        migrations.CreateModel(
            name="Pick",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("week", models.IntegerField()),
                ("season", models.IntegerField(default=2022)),
                (
                    "qb",
                    models.CharField(
                        blank=True, max_length=25, verbose_name="Quarterback"
                    ),
                ),
                (
                    "qb_id",
                    models.CharField(blank=True, default="", max_length=20, null=True),
                ),
                ("qb_points", models.FloatField(default=0.0)),
                (
                    "rb",
                    models.CharField(
                        blank=True, max_length=25, verbose_name="Running back"
                    ),
                ),
                (
                    "rb_id",
                    models.CharField(blank=True, default="", max_length=20, null=True),
                ),
                ("rb_points", models.FloatField(default=0.0)),
                (
                    "wr",
                    models.CharField(
                        blank=True, max_length=25, verbose_name="Wide receiver"
                    ),
                ),
                (
                    "wr_id",
                    models.CharField(blank=True, default="", max_length=20, null=True),
                ),
                ("wr_points", models.FloatField(default=0.0)),
                (
                    "te",
                    models.CharField(
                        blank=True, max_length=25, verbose_name="Tight end"
                    ),
                ),
                (
                    "te_id",
                    models.CharField(blank=True, default="", max_length=20, null=True),
                ),
                ("te_points", models.FloatField(default=0.0)),
                (
                    "defense",
                    models.CharField(blank=True, max_length=25, verbose_name="Defense"),
                ),
                (
                    "defense_id",
                    models.CharField(blank=True, default="", max_length=20, null=True),
                ),
                ("defense_points", models.FloatField(default=0.0)),
                ("total_points", models.FloatField(default=0.0)),
                (
                    "pick_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date Picked"),
                ),
                (
                    "team",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="picks",
                        to="ffl.fantasyteam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="League",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("password", models.CharField(max_length=150)),
                (
                    "admins",
                    models.ManyToManyField(
                        related_name="admins", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="fantasyteam",
            name="league",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to="ffl.league",
            ),
        ),
        migrations.AddField(
            model_name="fantasyteam",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Defense",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("week", models.IntegerField(verbose_name="Week")),
                ("season", models.IntegerField(default=2022, verbose_name="Season")),
                (
                    "fantasy_points",
                    models.DecimalField(
                        decimal_places=2, max_digits=13, verbose_name="Fantasy Points"
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="defenses",
                        to="ffl.team",
                    ),
                ),
            ],
        ),
    ]
