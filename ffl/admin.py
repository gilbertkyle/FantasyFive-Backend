from django.contrib import admin
from django.db import models
from .models import League, FantasyTeam, Pick, Player, PlayerWeek, Team, Defense

# Register your models here.


admin.site.register(League)
admin.site.register(FantasyTeam)
admin.site.register(Pick)
admin.site.register(Player)
admin.site.register(PlayerWeek)
admin.site.register(Team)
admin.site.register(Defense)
