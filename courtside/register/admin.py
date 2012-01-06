from django.contrib import admin
from register.models import Player, Sport


class PlayerAdmin(admin.ModelAdmin):
	pass

class SportAdmin(admin.ModelAdmin):
	pass


admin.site.register(Player, PlayerAdmin)
admin.site.register(Sport, SportAdmin)