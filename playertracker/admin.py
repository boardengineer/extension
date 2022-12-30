from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from playertracker.models import Player, Relic, Card, MapNode, MapEdge

#TokenAdmin.raw_id_fields = ['user']

# Register your models here.
class PlayerAdmin(admin.ModelAdmin):
    pass

class RelicAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    pass

class MapNodeAdmin(admin.ModelAdmin):
    pass

class MapEdgeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Player, PlayerAdmin)
admin.site.register(Relic, RelicAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(MapNode, MapNodeAdmin)
admin.site.register(MapEdge, MapEdgeAdmin)
