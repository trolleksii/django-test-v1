from django.contrib import admin

from .models import Team, HappyTeamUser

admin.site.register(Team)
admin.site.register(HappyTeamUser)
