from django.urls import include,path,re_path
from rest_framework import routers
from playertracker.views import player_list,PlayerList,PlayerViewSet

router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('players', player_list),
    re_path(r'^(?P<twitch_username>.+)/$', PlayerList.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
