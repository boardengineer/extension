from django.urls import include,path,re_path
from playertracker.views import decision_query, readonly_player_list, update_player_view, vote_view

urlpatterns = [
    re_path('vote/', vote_view),
    re_path(r'^(?P<channel_id>\w+)/$', readonly_player_list),
    re_path(r'^decision/(?P<prompt_id>\w+)/$', decision_query),
    re_path('', update_player_view),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
