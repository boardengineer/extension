from django.shortcuts import render
from rest_framework import generics,status,viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from playertracker.models import Player
from playertracker.serializers import PlayerSerializer,NukingPlayerSerializer

# Create your views here.
class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
class NukingPlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = NukingPlayerSerializer
 
class PlayerList(generics.ListAPIView):
    serializer_class = PlayerSerializer

    def get_queryset(self):
        twitch_username = self.kwargs['twitch_username']
        return Player.objects.filter(twitch_username=twitch_username)

@api_view(['GET','PUT','DELETE'])
def player_list(request):
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return Response(status=statusl.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','DELETE'])
def nuking_player_list(request):
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return Response(status=statusl.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NukingPlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
