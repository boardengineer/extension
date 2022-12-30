from django.shortcuts import render
from rest_framework import generics,status,viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from playertracker.models import Player
from playertracker.serializers import PlayerSerializer,NukingPlayerSerializer
from users.models import User

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def readonly_player_list(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        player = Player.objects.get(user=user)
    except Player.DoesNotExist:
        return Response(status=stats.HTTP_404_NOT_FOUND)

    serializer = PlayerSerializer(player, context={'request':request})
    return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_player_view(request):
    try:
        player = Player.objects.get(user=request.user)
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
