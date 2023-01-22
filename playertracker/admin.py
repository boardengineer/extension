from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from playertracker.models import Card, DecisionOption, DecisionPrompt, DecisionVote, MapEdge, MapNode, Player, Relic

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

class DecisionOptionAdmin(admin.ModelAdmin):
    pass

class DecisionPromptAdmin(admin.ModelAdmin):
    pass

class DecisionVoteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Player, PlayerAdmin)
admin.site.register(Relic, RelicAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(DecisionOption, DecisionOptionAdmin)
admin.site.register(DecisionPrompt, DecisionPromptAdmin)
admin.site.register(DecisionVote, DecisionVoteAdmin)
admin.site.register(MapNode, MapNodeAdmin)
admin.site.register(MapEdge, MapEdgeAdmin)
