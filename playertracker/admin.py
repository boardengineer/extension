from django.contrib import admin
from playertracker.models import Player, Relic

# Register your models here.
class PlayerAdmin(admin.ModelAdmin):
    pass

class RelicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Player, PlayerAdmin)
admin.site.register(Relic, RelicAdmin)
