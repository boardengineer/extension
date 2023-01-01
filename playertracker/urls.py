from django.urls import include,path,re_path
from playertracker.views import readonly_player_list,update_player_view

urlpatterns = [
    re_path(r'^(?P<channel_id>\w+)/$', readonly_player_list),
    re_path('', update_player_view),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
